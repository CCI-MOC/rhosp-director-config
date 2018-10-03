#!/bin/sh

openstack overcloud container image prepare \
  --namespace registry.access.redhat.com/rhosp13 \
  --push-destination 192.168.255.1:8787 \
  --prefix openstack- \
  --tag-from-label {version}-{release} \
  --output-env-file $PWD/patches/docker/overcloud_images.yaml \
  --output-images-file $PWD/local_registry_images.yaml

openstack overcloud container image upload \
  --config-file  $PWD/local_registry_images.yaml \
  --verbose

# Patch the stock images with our local changes
./scripts/build-images-wrapper -o $PWD/templates/overcloud_images.yaml --push
