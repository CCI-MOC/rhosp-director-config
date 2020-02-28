'''Tests that apply only to controllers.'''

import pytest
import testinfra

import helpers

testinfra_hosts = ['ansible://controller']
controller_processes = ['mysqld', 'beam.smp', 'redis-server']
controller_bundles = [
    'haproxy-bundle-docker',
    'redis-bundle-docker',
    'galera-bundle-docker',
    'rabbitmq-bundle-docker',
]

controller_containers = [
    'aodh_api',
    'aodh_evaluator',
    'aodh_listener',
    'aodh_notifier',
    'barbican_api',
    'barbican_keystone_listener',
    'barbican_worker',
    'ceilometer_agent_central',
    'ceilometer_agent_notification',
    'cinder_api',
    'cinder_api_cron',
    'cinder_scheduler',
    'clustercheck',
    'ec2_api',
    'ec2_api_metadata',
    'glance_api',
    'gnocchi_api',
    'gnocchi_metricd',
    'gnocchi_statsd',
    'heat_api',
    'heat_api_cfn',
    'heat_api_cron',
    'heat_engine',
    'horizon',
    'iscsid',
    'keystone',
    'keystone_cron',
    'logrotate_crond',
    'memcached',
    'neutron_api',
    'neutron_ovs_agent',
    'nova_api',
    'nova_api_cron',
    'nova_conductor',
    'nova_consoleauth',
    'nova_metadata',
    'nova_placement',
    'nova_scheduler',
    'nova_vnc_proxy',
    'octavia_api',
    'octavia_health_manager',
    'octavia_housekeeping',
    'octavia_worker',
    'panko_api',
    'sahara_api',
    'sahara_engine',
]


@pytest.mark.parametrize('comm', controller_processes)
def test_process_running(host, comm):
    '''Test that a specific command is running.

    Normally we would just test that the appropriate container is running,
    but PCS bundled resources a bit odd.  It's possible that the container can
    be running but the service itself is stopped.
    '''

    return helpers.test_command_running(host, comm)


def test_mysqld_responding(host):
    '''Verify that the database is responding.

    Connect to the database and send "select 1" to verify that
    the database is accepting connections and processing requests.
    '''

    containers = host.docker.get_containers(name='galera-bundle')
    for container in containers:
        res = host.docker.run(
            f'docker exec {container.name} mysql -e "select 1"')
        assert res.exit_status == 0


@pytest.mark.parametrize('container', controller_containers)
def test_container_running(host, container):
    '''Verify that containers are running and healthy'''
    return helpers.test_container_running(host, container)


@pytest.mark.parametrize('bundle', controller_bundles)
def test_bundle_running(bundle):
    '''Verify all members of a bundled resource are running'''
    controllers = testinfra.get_hosts(['ansible://controller'])
    count = len(controllers)
    container_names = ['{}-{}'.format(bundle, i) for i in range(count)]
    containers = []

    for name in container_names:
        for host in controllers:
            try:
                container = host.docker(name)
                if container.is_running:
                    print(f'found container {name} '
                          f'on host {host.backend.hostname}')
                    containers.append(container)
                    break
            except AssertionError:
                continue
        else:
            pytest.fail(f'container {name} is not running on any host')

    for container in containers:
        info = container.inspect()
        if 'Health' in info['State']:
            assert info['State']['Health']['Status'] == 'healthy'
