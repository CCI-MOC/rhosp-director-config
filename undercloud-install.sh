#!/bin/sh

openstack undercloud install

#if sudo ovs-vsctl list-ports br-ctlplane | grep ibft0; then
#	sudo ovs-vsctl del-port br-ctlplane ibft0
#	sudo ovs-vsctl add-port br-ctlplane vlan258
#fi
