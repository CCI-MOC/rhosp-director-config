'''Test OpenStack API endpoints.

These tests require valid credentials in your environment.'''

import pytest

simple_services = [
    'compute',
    'network',
    'placement',
    'volumev3',
    'identity',
    'image',
    'object-store',
]

request_paths = {
    'identity': '/v3/auth/system',
    'volumev3': '/types',
    'image': '/v2/info/import',
}


@pytest.mark.parametrize('service_type', simple_services)
def test_simple_api(sdk, service_type):
    '''Verify that API endpoints return a successful HTTP status'''

    endpoint = sdk.endpoint_for(service_type, interface='public')
    url = '{}{}'.format(endpoint, request_paths.get(service_type, ''))
    print(f'{service_type} endpoint {endpoint} url {url}')

    saved_err = None

    try:
        res = sdk.session.get(url)
        print(res.text)
    except Exception as err:
        saved_err = err
    else:
        assert res.status_code in [200, 204]

    if saved_err:
        pytest.fail(
            f'request to {url} for {service_type} failed with: {saved_err}')
