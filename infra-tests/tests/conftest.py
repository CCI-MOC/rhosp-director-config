'''Add 'hostname' and 'description' columns and drop the 'Links' column.

Via https://github.com/pytest-dev/pytest-html'''

import openstack
import pytest

from py.xml import html


def pytest_html_results_table_header(cells):
    cells.insert(1, html.th('Description'))
    cells.insert(1, html.th('Hostname',
                            class_='sortable hostname',
                            col='hostname'))
    cells.pop()


def pytest_html_results_table_row(report, cells):
    cells.insert(1, html.td(report.description))
    cells.insert(1, html.td(report.hostname, col='col-hostname'))
    cells.pop()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if 'host' in item.funcargs:
        report.hostname = item.funcargs['host'].backend.hostname
    else:
        report.hostname = '<none>'

    if item.function.__doc__ is not None:
        report.description = str(item.function.__doc__.splitlines()[0])
    else:
        report.description = ''


@pytest.fixture(scope='module')
def sdk():
    try:
        return openstack.connect()
    except Exception as err:
        pytest.skip(f'unable to authenticate to openstack: {err}')
