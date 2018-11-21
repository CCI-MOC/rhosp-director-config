#!/usr/bin/env python

from __future__ import print_function

import argparse
import collections
import sys
import yaml


class UnsortableList(list):
    def sort(self, *args, **kwargs):
        pass


class UnsortableOrderedDict(collections.OrderedDict):
    def items(self, *args, **kwargs):
        return UnsortableList(
            collections.OrderedDict.items(self, *args, **kwargs))


yaml.add_representer(UnsortableOrderedDict,
                     yaml.representer.SafeRepresenter.represent_dict)


def kvarg(v):
    if '=' not in v:
        raise ValueError('arguments must be of the form k=v')

    k, v = v.split('=')

    if v.lower() in ('true', 'false'):
        v = v.lower() == 'true'
    elif v.isdigit():
        v = int(v)

    return (k, v)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--output', '-o')

    p.add_argument('--tag', '-t',
                   action='append',
                   default=[])
    p.add_argument('--network', '-n',
                   action='append',
                   default=[])
    p.add_argument('--remove-network',
                   action='append',
                   default=[])
    p.add_argument('--service', '-s',
                   action='append',
                   default=[])
    p.add_argument('--remove-service', '-r',
                   action='append',
                   default=[])

    p.add_argument('--extra', '-x',
                   type=kvarg,
                   action='append',
                   default=[])

    p.add_argument('name')
    p.add_argument('roles',
                   default=[],
                   nargs='+')

    return p.parse_args()


def uniqify(l, exclude=None):
    if exclude is None:
        exclude = []

    seen = set()
    return [x for x in l if not (x in seen or seen.add(x))
            and x not in exclude]


def main():
    args = parse_args()

    extraconfig = [
        ('HostnameFormatDefault',
         '%stackname%-{}-%index%'.format(args.name.lower())),
        ('CountDefault', 1),
    ]

    services = []
    networks = []
    default_route_networks = []
    tags = []
    for role_file in args.roles:
        with open(role_file) as fd:
            role_spec = yaml.load(fd)
            for role in role_spec:
                services.extend(role.get('ServicesDefault', []))
                networks.extend(role.get('networks', []))
                tags.extend(role.get('tags', []))
                default_route_networks.extend(
                    role.get('default_route_networks', []))

    services.extend(args.service)
    networks.extend(args.network)
    tags.extend(args.tag)

    for kv in args.extra:
        extraconfig.append(kv)

    new_networks = sorted(uniqify(networks, exclude=args.remove_network))
    new_services = sorted(uniqify(services, exclude=args.remove_service))

    new_role = [
        UnsortableOrderedDict(
            (('name', args.name),) + tuple(extraconfig) + (
                ('tags', sorted(uniqify(tags))),
                ('networks', new_networks),
                ('default_route_networks',
                 sorted(uniqify(default_route_networks))),
                ('ServicesDefault', new_services),
            ))
    ]

    with (open(args.output, 'w') if args.output else sys.stdout) as fd:
        print(yaml.dump(new_role, default_flow_style=False), file=fd)


if __name__ == '__main__':
    main()
