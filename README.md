---
title: MOC OSP Director Configuration
---

## Hosts

This configuration will provision:

- 1 undercloud
- 3 controllers
- 2 compute nodes

## Networking

| Interface | VLAN | Tagged | CIDR              | DHCP? | Description         | Director network |
|-----------|------|--------|-------------------|-------|---------------------|------------------|
| eth0      | 4014 | N      |                   | Y     | foreman provisioning network | |
| eth1      | ?    | N      |                   | Y     | bmi provisioning network | |
| eth1      | 3700 | Y      | 192.168.16.0/22   | N     | ceph public network | Storage |
| eth2      | 105  | Y      | 192.12.185.0/24   | N     | public API/horizon | External |
| eth2      | 3702 | Y      | 192.168.32.0/22   | N     | openstack api network | InternalApi |
| eth2      | 3703 | Y      | 192.168.24.0/24   | N     | director control plane | ControlPlane |
| eth2      | 3704 | Y      | 192.168.12.0/22   | N     | tenant networks | Tenant |
| eth2      | 3803 | Y      | 128.31.28.0/24    | N     | floating ip | |

## Wrapper scripts

There are three wrapper scripts in this repository that simplify the
process of deploying RHOSP.

- `overcloud-prep.sh`

  Retrieves all the necessary Docker images from the remote repository
  and stores them into the local registry running on the undercloud
  host.

  It generates the `templates/overcloud_images.yaml` environment file
  that points the overcloud deploy at the local registry server.

- `overcloud-deploy.sh`

  Runs the actual overcloud deploy. Ensures that the environment files
  necessary to realize our overcloud configuration are provide on the
  deploy command line.

- `overcloud-continue.sh`

  When deploying onto pre-provisioned nodes, the individual nodes must
  poll the undercloud in order to receive their configuration.  This
  script automates that process, following the instructions in
  the [Director Installation and Usage][] guide.

[director installation and usage]: https://access.redhat.com/documentation/en-us/red_hat_openstack_platform/12/html-single/director_installation_and_usage/#sect-Polling_the_Metadata_Server

## Configuration files

- `templates/network/network_data.yaml`

  This overrides the stock list of overcloud networks. We disable the
  "storage management", since we're running all of our storage traffic
  over a single vlan.

- `templates/network/config/compute.yaml`
  
  Describes the network configuration of compute nodes.

- `templates/network/config/controller.yaml`

  Describes the network configuration of controllers.

- `templates/ceph-external.yaml`

  This configures the overcloud to use an existing Ceph cluster rather
  than deploying a Ceph service as part of the overcloud.

- `templates/deploy.yaml`

  This contains the bulk of our custom configuration (including
  information about network address ranges and vlan ids).

- `templates/services/horizon.yaml`

  This is a patched version of
  `/usr/share/openstack-tripleo-heat-templates/docker/services/horizon.yaml`
  that enables the Neutron LBaaS dashboard.

- `templates/extraconfig.yaml`

  Contains some post-deploy actions required to finalize the network
  configuration.

- `templates/enable-lbaas-ui.yaml`

  This replaces the stock `horizon.yaml` service template with our
  local override.

- `templates/swift-external.yaml`

  Configures the overcloud to use Ceph RadosGW for the object storage
  service, rather than deploying Swift as part of the overcloud
  install.

### Credentials

The file `templates/credentials.yaml` is required by the
`overcloud-deploy.sh` script, but it does not exist in this
repository.  This file contains all passwords, keys, and other secrets
required for the deployment.
