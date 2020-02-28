'''Tests that apply to the Pacemaker cluster.'''

import lxml.etree
import pytest
import testinfra

import helpers

testinfra_hosts = ['ansible://controller']


@pytest.fixture(scope='module')
def pcs_status():
    hosts = testinfra.get_hosts(['ansible://controller'])
    c1 = hosts[0]
    res = c1.run('pcs status xml')
    doc = lxml.etree.fromstring(res.stdout)
    return doc


@pytest.fixture(scope='module')
def pcs_nodes(pcs_status):
    return pcs_status.xpath('/crm_mon/nodes/node')


@pytest.fixture(scope='module')
def pcs_members(pcs_status):
    return pcs_status.xpath('/crm_mon/nodes/node[@type="member"]')


@pytest.fixture(scope='module')
def pcs_remotes(pcs_status):
    return pcs_status.xpath('/crm_mon/nodes/node[@type="remote"]')


@pytest.fixture(scope='module')
def pcs_resources(pcs_status):
    return pcs_status.xpath('/crm_mon/resources//resource')


@pytest.fixture(scope='module')
def pcs_failures(pcs_status):
    return pcs_status.xpath('/crm_mon/failures/failure')


@pytest.mark.parametrize('service_name', ['corosync', 'pacemaker'])
def test_service_active(host, service_name):
    '''Verify that services are running and enabled.'''
    return helpers.test_service_active(host, service_name)


def test_pcs_summary(pcs_status):
    '''Verify that there are no disabled or blocked resources'''
    res = pcs_status.xpath('/crm_mon/summary/resources_configured')[0]
    print(lxml.etree.tostring(res, pretty_print=True).decode('utf-8'))
    assert int(res.get('disabled')) == 0
    assert int(res.get('blocked')) == 0


def test_members_online(pcs_members):
    '''Verify that all pacemaker nodes are online'''
    for node in pcs_members:
        print(lxml.etree.tostring(node, pretty_print=True).decode('utf-8'))
        assert node.get('online') == 'true'
        assert node.get('unclean') == 'false'


def test_remotes_online(pcs_remotes):
    '''Verify that all pacemaker remotes are online'''
    for node in pcs_remotes:
        print(lxml.etree.tostring(node, pretty_print=True).decode('utf-8'))
        assert node.get('online') == 'true'
        assert node.get('unclean') == 'false'


def test_resources_healthy(pcs_resources):
    '''Verify that all resources are healthy'''
    for rsrc in pcs_resources:
        print(lxml.etree.tostring(rsrc, pretty_print=True).decode('utf-8'))
        assert rsrc.get('active') == 'true'
        assert rsrc.get('failed') == 'false'
        assert rsrc.get('role') in ['Started', 'Master', 'Slave']


def test_failures(pcs_failures):
    '''Verify that there are no failures'''
    print('\n'.join(
        lxml.etree.tostring(failure, pretty_print=True).decode('utf-8')
        for failure in pcs_failures
    ))
    assert len(pcs_failures) == 0
