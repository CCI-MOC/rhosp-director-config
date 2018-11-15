import re

re_hostname = re.compile('(?P<base>[^-]+)-(?P<position>\d+-\d+)-(?P<tail>).*')


def pos(host):
    mo = re_hostname.match(host)
    if not mo:
        raise ValueError('invalid hostname: {}'.format(host))

    return tuple(int(x) for x in mo.group('position').split('-'))


def filter_hostname_sort(v):
    return sorted(v, key=pos)


class FilterModule(object):
    filter_map = {
        'hostname_sort': filter_hostname_sort,
    }

    def filters(self):
        return self.filter_map
