'''Network tests that apply to all overcloud hosts'''

import pytest

import helpers

testinfra_hosts = ['ansible://overcloud']
overcloud_services = ['os-collect-config']


@pytest.mark.parametrize('service_name', overcloud_services)
def test_service_active(host, service_name):
    '''Verify that services are running and enabled'''
    return helpers.test_service_active(host, service_name)


def test_ovs_running(host):
    '''Verify that openvswitch is enabled and running'''
    return helpers.test_service_active(host, 'openvswitch')


def test_ovs_agent_running(host):
    '''Verify that the neutron_ovs_container is running'''
    return helpers.test_container_running(host, 'neutron_ovs_agent')


def test_ovs_responding(host):
    '''Verify that openvswitch is actually reponding to requests'''
    res = host.run('ovs-vsctl show')
    print('stdout:', res.stdout)
    print('stderr:', res.stderr)
    assert res.exit_status == 0


@pytest.mark.parametrize('bridge', ['br-ex', 'br-int', 'br-tun'])
def test_of_tables_exist(host, bridge):
    '''Verify that all OVS bridges have a non-empty flow table'''
    res = host.run(f'ovs-vsctl br-exists {bridge}')
    assert res.exit_status in [0, 2]
    if res.exit_status == 2:
        pytest.skip(f'bridge {bridge} does not exist on this host')

    res = host.run(f'ovs-ofctl dump-flows {bridge}')
    lines = res.stdout.splitlines()
    llen = len(lines)
    print(f'found {llen} lines of output')
    if llen > 5:
        print('\n'.join([lines[0], '...', lines[-1]]))
    else:
        print('\n'.join(lines))

    assert res.exit_status == 0
    assert len(res.stdout.strip()) != 0
