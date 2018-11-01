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
| eth0      | ? |        |                   |       | unused  ||
| eth1      | ? |        |                   |       | unused  ||
| eth2      | 3699    | N      |                   | Y     | foreman provisioning network | |
| eth2      | 105  | Y      | 192.12.185.0/24   | N     | public API/horizon | External |
| eth2      | 3702 | Y      | 192.168.32.0/22   | N     | openstack api network | InternalApi |
| eth2      | 3704 | Y      | 192.168.12.0/22   | N     | tenant networks | Tenant |
| eth2      | 3803 | Y      | 128.31.28.0/24    | N     | floating ip | |
| eth3      | 3700 | Y      | 192.168.16.0/22   | N     | ceph public network | Storage |

## Wrapper scripts

There are three wrapper scripts in this repository that simplify the
process of deploying RHOSP.

- `overcloud-prep.sh`

  Retrieves all the necessary Docker images from the remote repository
  and stores them into the local registry running on the undercloud
  host.

  It generates the `templates/overcloud_images.yaml` environment file
  that points the overcloud deploy at the local registry server.

  This script is responsible for generating any patched Docker images
  necessary for the deployment and pushing them into the local
  registry.

- `overcloud-deploy.sh`

  Runs the actual overcloud deploy. This takes care of generating some
  files (mostly credentials) from templates. Ensures that the
  environment files necessary to realize our overcloud configuration
  are provide on the deploy command line.

  Prior to running the `openstack overcloud deploy` command, this
  script packages up any patched puppet modules and ensures that they
  will be installed as part of the deploy process.

- `overcloud-continue.sh`

  When deploying onto pre-provisioned nodes, the individual nodes must
  poll the undercloud in order to receive their configuration.  This
  script automates that process, following the instructions in
  the [Director Installation and Usage][] guide.

[director installation and usage]: https://access.redhat.com/documentation/en-us/red_hat_openstack_platform/12/html-single/director_installation_and_usage/#sect-Polling_the_Metadata_Server

## Configuration files

- `templates/network/network_data.yaml`

  This overrides the stock list of overcloud networks. We disable the
  "storage management" network, since we're running all of our storage
  traffic over a single vlan.

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

- `templates/postconfig.yaml`

  Contains post-deploy actions that take care of:

  - Finalizing the network configuration for br-ex
  - Creating the necessary keystone resources to support openid
    federation
  - Creating some Nova flavors

- `templates/swift-external.yaml`

  Configures the overcloud to use Ceph RadosGW for the object storage
  service, rather than deploying Swift as part of the overcloud
  install.

- `templates/services/patch-puppet-modules.yaml`

  Deploys patched puppet modules (from `patches/puppet-modules`) onto
  the overcloud nodes.  This is a replacement for the existing
  [DeployArtifacts][] feature, which was not suitable for this
  purpose.

  [deployartifacts]: http://hardysteven.blogspot.com/2016/08/tripleo-deploy-artifacts-and-puppet.html

- `templates/single-signon.yaml`

  Configuration for enabling Keystone federated authentication.

### Credentials

The file `credentials.yaml` is generated at deploy time from
`credentials.yaml.in`.  This pulls passwords and other secrets from
Bitwarden.

## Patches

We are carrying several patches as part of our deployment.

### Keystone Docker Image

We are using a patched version of the Keystone docker image that
includes the `mod_auth_openidc` package to support Keystone
federation.

### Horizon Docker Image

We are using a patched version of the Horizon docker image in order to
support our custom theme.

### Puppet modules

While not included in this repository, we are also making use of
patches versions of `puppet-keystone` and `puppet-tripleo` in order to
support Keystone federation.

The changes can all be found at
https://review.openstack.org/#/q/status:open+topic:feature/keystone/openidc.

