'''Common code that is used by multiple test collections.'''

import json
import pytest


def test_container_running(host, container_name):
    '''Test that a container is running and healthy.'''

    container = host.docker(container_name)
    try:
        info = container.inspect()
    except AssertionError:
        info = None

    if info is None:
        pytest.fail(f'container {container_name} is not running')
    print(json.dumps(info['State'], indent=2))
    assert container.is_running
    if 'Health' in info['State']:
        assert info['State']['Health']['Status'] == 'healthy'


def test_command_running(host, comm, expected=None):
    '''Test that a specific command is running.'''

    procs = host.process.filter(comm=comm)
    print('\n'.join(f'{p.pid} {p.comm} {p.lstart}'
                    for p in procs))

    if expected is not None:
        assert len(procs) == expected
    else:
        assert len(procs) > 0


def test_service_active(host, service_name):
    '''Test that a service is running and enabled.'''
    service = host.service(service_name)
    assert service.is_running
    assert service.is_enabled
