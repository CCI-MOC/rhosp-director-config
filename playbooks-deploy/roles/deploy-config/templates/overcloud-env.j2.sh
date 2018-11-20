#!/bin/sh
#
# This file is generated with Ansible. Any changes made here will be
# lost.

export ControllerDeployedServer_hosts="
{% for host in groups.controller %}
{{host}}
{% endfor %}
"
export ComputeDeployedServer_hosts="
{% for host in groups.compute %}
{{host}}
{% endfor %}
"
export NetworkerDeployedServer_hosts="
{% for host in groups.network %}
{{host}}
{% endfor %}
"

export OVERCLOUD_ROLES="ControllerDeployedServer ComputeDeployedServer NetworkerDeployedServer"
export OVERCLOUD_HOSTS="$ControllerDeployedServer_hosts $ComputeDeployedServer_hosts $NetworkerDeployedServer_hosts"
