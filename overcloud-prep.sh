#!/bin/sh

tag=$(openstack overcloud container image tag discover \
  --image registry.access.redhat.com/rhosp12/openstack-base:latest \
  --tag-from-label version-release)

echo "using tag: $tag"

openstack overcloud container image prepare \
  --namespace=registry.access.redhat.com/rhosp12 \
  --prefix=openstack- \
  --tag=$tag \
  --output-images-file $PWD/local_registry_images.yaml

openstack overcloud container image upload \
  --config-file  $PWD/local_registry_images.yaml \
  --verbose

openstack overcloud container image prepare \
  --namespace=192.168.24.1:8787/rhosp12 \
  --prefix=openstack- \
  --tag=$tag \
  --output-env-file=$PWD/templates/overcloud_images.yaml
