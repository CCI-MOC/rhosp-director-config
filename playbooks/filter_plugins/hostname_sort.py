import re

re_hostname = re.compile(r'overcloud-(?P<hosttype>[^-]+)-(?P<position>\d+)')


def pos(host, hostvars):
    ooo_name = hostvars[host]['ooo_name']
    ooo_seq = int(ooo_name.split('-')[-1])
    return ooo_seq


def filter_hostname_sort(v, hostvars=None):
    return sorted(v, key=lambda host: pos(host, hostvars))


class FilterModule(object):
    filter_map = {
        'hostname_sort': filter_hostname_sort,
    }

    def filters(self):
        return self.filter_map
