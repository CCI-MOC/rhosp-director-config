#!/bin/sh

export OVERCLOUD_ROLES="ControllerDeployedServer ComputeDeployedServer"
export ControllerDeployedServer_hosts="kumo-control-01 kumo-control-02 kumo-control-03"
export ComputeDeployedServer_hosts="kumo-compute-01 kumo-compute-02"

/usr/share/openstack-tripleo-heat-templates/deployed-server/scripts/get-occ-config.sh
