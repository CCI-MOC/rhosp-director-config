#!/bin/sh

TEMPLATES=/usr/share/openstack-tripleo-heat-templates

# When passing environment files (`-e ...`) to the `overcloud deploy`
# command, order is important! Your custom configuration
# (`$PWD/templates/deploy.yaml` in this script) should come *last*,
# in particular because the network interface configuration is
# initialized by `deployed-server-environment.yaml`.  If you custom
# configuration were provided first, the network interface
# configuration you provide would be lost and replaced with the
# defaults.

openstack overcloud deploy \
	--templates $TEMPLATES \
	--disable-validations --deployed-server \
	--libvirt-type kvm \
	--ntp-server pool.ntp.org \
	-n $PWD/templates/network/network_data.yaml \
	-e $TEMPLATES/environments/network-isolation.yaml \
	-e $TEMPLATES/environments/deployed-server-environment.yaml \
	-e $TEMPLATES/environments/deployed-server-bootstrap-environment-rhel.yaml \
	-e $TEMPLATES/environments/deployed-server-pacemaker-environment.yaml \
	-r $TEMPLATES/deployed-server/deployed-server-roles-data.yaml \
	-e $PWD/templates/deploy.yaml \
	-e $PWD/template/ceph-external.yaml \
	-e $PWD/templates/credentials.yaml
