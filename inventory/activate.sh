#!/bin/sh


pushd ${BASH_SOURCE[0]%/*}
export ANSIBLE_INVENTORY="$(pwd)/hosts.yml"
popd
