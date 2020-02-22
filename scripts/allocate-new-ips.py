#!/usr/bin/python

import click
import logging
import re
import yaml

from ipaddress import ip_address as IPAddress
from ipaddress import ip_network as IPNetwork

LOG = logging.getLogger(__name__)

ROLES = [
    'ControllerDeployedServer',
    'ComputeDeployedServer',
    'NetworkerDeployedServer',
]

NETWORKS = {
    'internal_api': IPNetwork('172.16.32.0/19'),
    'storage': IPNetwork('192.168.0.0/19'),
    'tenant': IPNetwork('172.16.64.0/19'),
    'external': IPNetwork('129.10.5.0/24'),
    'ctlplane': IPNetwork('172.16.0.0/19'),
}

re_ip = re.compile(r'[^\d](\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[^\d]')


def find_existing_ips(config):
    addresses = []
    allocated = {k: set() for k in NETWORKS}

    defaults = config['parameter_defaults']

    # get list of vips
    for k, v in defaults.items():
        if isinstance(v, list):
            addresses.append(v[0]['ip_address'])

    # get node addresses
    for role in ROLES:
        rolekey = f'{role}IPs'
        for network in NETWORKS:
            if network not in defaults[rolekey]:
                continue

            addresses.extend(defaults[rolekey][network])

    for addr in addresses:
        addr = IPAddress(addr)
        for name, cidr in NETWORKS.items():
            if addr in cidr:
                allocated[name].add(addr)

    return allocated


@click.command()
@click.option('-f', '--static-ip-file',
              default='templates/use_fixed_ips.yaml',
              type=click.File('r'))
@click.option('-c', '--count', type=int)
def main(static_ip_file, count):
    logging.basicConfig(level=logging.INFO)
    with static_ip_file:
        static_ip_config = yaml.safe_load(static_ip_file)

    LOG.info('scanning existing addresses')
    allocated = find_existing_ips(static_ip_config)
    compute = (
        static_ip_config['parameter_defaults']['ComputeDeployedServerIPs']
    )

    LOG.info('allocating new addresses')
    for network in ['ctlplane', 'storage', 'tenant', 'internal_api']:
        i = count
        for j, addr in enumerate(NETWORKS[network].hosts()):
            # skip the first 10 addresses in the network
            # in case we have routers or something...
            if j < 10:
                continue
            if addr not in allocated[network]:
                allocated[network].add(addr)
                compute[network].append(str(addr))
                i -= 1
                if not i:
                    break
        else:
            raise click.ClickException(
                f'ran out of ip addresses for {network} network')

    print(yaml.safe_dump(static_ip_config, default_flow_style=False))


if __name__ == '__main__':
    main()
