'''Tests that apply only to compute nodes.'''

import pytest

import helpers

testinfra_hosts = ['ansible://compute']
compute_containers = [
    'nova_libvirt',
    'nova_compute',
    'iscsid',
    'nova_migration_target',
    'nova_virtlogd',
    'logrotate_crond',
    'ceilometer_agent_compute'
]


def test_libvirt_responding(host):
    '''Verify that libvirtd is responding to requests'''
    res = host.run('virsh uri')
    print('stdout:', res.stdout)
    print('stderr:', res.stderr)
    assert res.exit_status == 0
    assert res.stdout.strip() == 'qemu:///system'


@pytest.mark.parametrize('container', compute_containers)
def test_container_running(host, container):
    '''Verify that containers are running and healthy'''
    return helpers.test_container_running(host, container)
