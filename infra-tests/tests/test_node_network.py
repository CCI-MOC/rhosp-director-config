'''Tests that apply only to network hosts.'''

import pytest

import helpers

testinfra_hosts = ['ansible://network']
network_containers = [
    'neutron_ovs_agent',
    'neutron_dhcp',
    'neutron_l3_agent',
    'neutron_metadata_agent',
    'logrotate_crond',
]


@pytest.mark.parametrize('container_name', network_containers)
def test_container_running(host, container_name):
    '''Verify that containers are running and healthy'''
    return helpers.test_container_running(host, container_name)
