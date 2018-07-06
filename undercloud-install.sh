#!/bin/sh

openstack undercloud install

if sudo ovs-vsctl list-ports br-ctlplane | grep eth1; then
	sudo ovs-vsctl del-port br-ctlplane eth1
	sudo ovs-vsctl add-port br-ctlplane vlan3703
fi
