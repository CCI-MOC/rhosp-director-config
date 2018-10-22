#!/bin/sh

export OVERCLOUD_ROLES="ControllerDeployedServer ComputeDeployedServer NetworkerDeployedServer"
export ControllerDeployedServer_hosts="
neu-3-39-control3.kzn.moc
neu-5-39-control2.kzn.moc
neu-15-39-control1.kzn.moc
"
export ComputeDeployedServer_hosts="
neu-3-34-stackcomp.kzn.moc
neu-3-35-stackcomp.kzn.moc
neu-3-36-stackcomp.kzn.moc
neu-3-37-stackcomp.kzn.moc
neu-3-38-stackcomp.kzn.moc
neu-5-34-stackcomp.kzn.moc
neu-5-35-stackcomp.kzn.moc
neu-5-36-stackcomp.kzn.moc
neu-5-37-stackcomp.kzn.moc
neu-5-38-stackcomp.kzn.moc
neu-15-34-stackcomp.kzn.moc
neu-15-35-stackcomp.kzn.moc
neu-15-36-stackcomp.kzn.moc
neu-15-37-stackcomp.kzn.moc
neu-15-38-stackcomp.kzn.moc
"
export NetworkerDeployedServer_hosts="
neu-19-11-nc1.kzn.moc
neu-17-11-nc2.kzn.moc
"

/usr/share/openstack-tripleo-heat-templates/deployed-server/scripts/get-occ-config.sh
