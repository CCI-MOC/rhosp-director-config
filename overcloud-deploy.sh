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

# Generate files
make TEMPLATES=$TEMPLATES

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
	#-e $TEMPLATES/environments/services/octavia.yaml

	# Disable octavia
	-e $PWD/templates/disable-octavia.yml

	# Enable Sahara
	-e $TEMPLATES/environments/services/sahara.yaml

	# Enable OpenIDC federation
	-e $TEMPLATES/environments/enable-federation-openidc.yaml

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

	# Most of our custom configuration.
	-e $PWD/templates/deploy.yaml
	-e $PWD/templates/credentials.yaml
	-e $PWD/templates/fencing.yaml

	# Static ip assignment
	-e $PWD/templates/hostnamemap.yaml
	-e $PWD/templates/deployedserverportmap.yaml
)

if [ -d patches/puppet-modules ]; then
	echo "archiving puppet modules..."
	tar -cz -f puppet-modules.tar.gz -C patches/puppet-modules .

	echo "uploading puppet modules..."
	upload-swift-artifacts \
		-f puppet-modules.tar.gz \
		--environment $PWD/templates/puppet_modules.yaml

	sed -i s/DeployArtifactURLs/PuppetModuleUrls/ \
		$PWD/templates/puppet_modules.yaml

	deploy_args+=(-e $PWD/templates/puppet_modules.yaml)
fi

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
