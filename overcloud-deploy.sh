#!/bin/bash

set -e

if [ "$OS_CLOUDNAME" != "undercloud" ]; then
	echo "ERROR: missing undercloud credentials" >&2
	exit 1
fi

if [ -d patches/tripleo-heat-templates ]; then
	TEMPLATES=$PWD/patches/tripleo-heat-templates
else
	TEMPLATES=/usr/share/openstack-tripleo-heat-templates
fi

# This is necessary to work around bugs #1645503 and #1645134
. ./overcloud-env.sh
bash $TEMPLATES/deployed-server/scripts/enable-ssh-admin.sh

# When passing environment files (`-e ...`) to the `overcloud deploy`
# command, order is important! Your custom configuration
# (`$PWD/templates/deploy.yaml` in this script) should come *last*,
# in particular because the network interface configuration is
# initialized by `deployed-server-environment.yaml`.  If your custom
# configuration were provided first, the network interface
# configuration you provide would be lost and replaced with the
# defaults.

deploy_args=(
	# network_data.yaml defines a custom network configuration. In 
	# particular, we disable the StorageMgmt network, since we're not
	# using it.
	-n $PWD/templates/network/network_data.yaml

	# Enable network isolation (using different networks for different
	# purposes).
	-e $TEMPLATES/environments/network-isolation.yaml

	# Enable deployment onto pre-provisioned servers.
	-e $TEMPLATES/environments/deployed-server-environment.yaml
	-e $TEMPLATES/environments/deployed-server-bootstrap-environment-rhel.yaml
	-e $TEMPLATES/environments/deployed-server-pacemaker-environment.yaml
	-r $PWD/roles_data.yaml

	# Enable TLS for public endpoints.
	-e $TEMPLATES/environments/ssl/enable-tls.yaml
	-e $TEMPLATES/environments/tls-endpoints-public-dns.yaml

	# Enable Neutron Octavia load-balancer service.
	-e $TEMPLATES/environments/services/octavia.yaml

	# Enable barbican
	-e $TEMPLATES/environments/services/barbican.yaml
	-e $TEMPLATES/environments/barbican-backend-simple-crypto.yaml

	# Enable Sahara
	-e $TEMPLATES/environments/services/sahara.yaml

	# Enable EC2 API
	-e $TEMPLATES/environments/services/ec2-api.yaml

	# Enable OpenIDC federation
	#-e $TEMPLATES/environments/enable-federation-openidc.yaml

	# Use Docker registry on the undercloud.
	-e $PWD/templates/overcloud_images.yaml

	# Enable keystone federation
	-e $PWD/templates/single-signon.yaml

	# Enable external Ceph cluster
	-e $TEMPLATES/environments/ceph-ansible/ceph-ansible-external.yaml
	-e $PWD/templates/ceph-external.yaml

	# Enable external Ceph RadosGW (object storage)
	-e $TEMPLATES/environments/swift-external.yaml
	-e $PWD/templates/swift-external.yaml

	# Disable snmp (to be configured outside of Director)
	-e $PWD/templates/disable-snmp.yaml

	# Most of our custom configuration.
	-e $PWD/templates/deploy.yaml
	-e $PWD/templates/services.yaml
	-e $PWD/templates/rolecount.yaml
	-e $PWD/templates/credentials.yaml
	-e $PWD/templates/fencing.yaml

	# Static ip assignment
	-e $PWD/templates/hostnamemap.yaml
	-e $PWD/templates/deployedserverportmap.yaml

	# per https://access.redhat.com/support/cases/#/case/02552401
	-e $PWD/templates/use_fixed_ips.yaml
)

if [ -f local_deploy_config.sh ]; then
	. local_deploy_config.sh
fi

openstack overcloud deploy \
	--templates $TEMPLATES \
	--disable-validations --deployed-server \
	--libvirt-type kvm \
	--ntp-server pool.ntp.org \
	"${deploy_args[@]}" \
	"$@"
