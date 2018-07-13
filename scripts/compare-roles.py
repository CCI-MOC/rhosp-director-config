#!/usr/bin/env python

from __future__ import print_function

import argparse
import yaml


def parse_args():
    p = argparse.ArgumentParser()

    p.add_argument('role1')
    p.add_argument('role2')

    return p.parse_args()


def uniqify(l):
    seen = set()
    return [x for x in l if not (x in seen or seen.add(x))]


def main():
    args = parse_args()

    with open(args.role1) as fd:
        role1 = yaml.load(fd)

    with open(args.role2) as fd:
        role2 = yaml.load(fd)

    role1_services = set(role1[0]['ServicesDefault'])
    role2_services = set(role2[0]['ServicesDefault'])

    print('Services in {} but not in {}:'.format(args.role1, args.role2))
    print(yaml.dump(sorted(role1_services-role2_services),
                    default_flow_style=False))

    print()
    print('Services in {} but not in {}:'.format(args.role2, args.role1))
    print(yaml.dump(sorted(role2_services-role1_services),
                    default_flow_style=False))


if __name__ == '__main__':
    main()
