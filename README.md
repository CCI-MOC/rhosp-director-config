---
title: Boston University MoC Director Configuration
---

## Hosts

This configuration will provision:

- 1 undercloud
- 3 controllers
- 2 compute nodes

## Networking

| Interface | VLAN | Tagged | CIDR              | DHCP? | Description         | Director network |
|-----------|------|--------|-------------------|-------|---------------------|------------------|
| eth0      |      | N      | 192.168.122.0/24  | Y     | access from vm host | |
| eth1      | 4014 | N      |                   | Y     | foreman provisioning network | |
| eth2      | ?    | N      |                   | Y     | bmi provisioning network | |
| eth2      | 3700 | Y      | 192.168.16.0/22   | N     | ceph public network | Storage |
| eth3      | 105  | Y      | 192.12.185.0/24   | N     | public API/horizon | External |
| eth3      | 3702 | Y      | 192.168.32.0/22   | N     | openstack api network | InternalApi |
| eth3      | 3703 | Y      | 192.168.24.0/24   | N     | director control plane | ControlPlane |
| eth3      | 3704 | Y      | 192.168.28.0/22   | N     | tenant networks | Tenant |
| eth3      | 3803 | Y      | 128.31.28.0/24    | N     | floating ip | |

