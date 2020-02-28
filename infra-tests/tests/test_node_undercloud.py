'''Tests that apply only to the undercloud.'''

import json
import pytest

import helpers

testinfra_hosts = ['ansible://undercloud']
undercloud_services = ['mariadb', 'openstack-heat-engine']


@pytest.mark.parametrize('service_name', undercloud_services)
def test_service_active(host, service_name):
    '''Verify that services are running and enabled'''
    return helpers.test_service_active(host, service_name)


def test_stack_health(host):
    '''Verify that the overcloud stack is healthy'''
    res = host.run('. ~/stackrc; openstack stack list -f json')
    print(res.stdout)
    stacks = json.loads(res.stdout)
    assert len(stacks) == 1
    assert stacks[0]['Stack Name'] == 'overcloud'
    assert stacks[0]['Stack Status'] in ['UPDATE_COMPLETE', 'CREATE_COMPLETE']
