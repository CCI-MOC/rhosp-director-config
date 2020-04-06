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

# Ensure that templates are up-to-date
(cd playbooks; ansible-playbook deploy.yml)

# This is necessary to work around bugs #1645503 and #1645134
. ./overcloud-env.sh
bash $TEMPLATES/deployed-server/scripts/enable-ssh-admin.sh

. overcloud-deploy-args.sh

openstack overcloud deploy \
	--templates $TEMPLATES \
	--disable-validations --deployed-server \
	--libvirt-type kvm \
	--ntp-server pool.ntp.org \
	"${deploy_args[@]}" \
	"$@"
