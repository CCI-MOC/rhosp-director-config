'''Test OpenStack compute API.

These tests require valid credentials in your environment.'''


def test_hypervisors_up(sdk):
    for hv in sdk.list_hypervisors():
        assert hv['state'] == 'up'
