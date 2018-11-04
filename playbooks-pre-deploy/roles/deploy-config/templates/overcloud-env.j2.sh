#!/bin/sh

export ControllerDeployedServer_hosts="
{% for host in groups.controller|hostname_sort %}
{{host}}
{% endfor %}
"
export ComputeDeployedServer_hosts="
{% for host in groups.compute|hostname_sort %}
{{host}}
{% endfor %}
"
export NetworkerDeployedServer_hosts="
{% for host in groups.network|hostname_sort %}
{{host}}
{% endfor %}
"

export OVERCLOUD_ROLES="ControllerDeployedServer ComputeDeployedServer NetworkerDeployedServer"
export OVERCLOUD_HOSTS="$ControllerDeployedServer_hosts $ComputeDeployedServer_hosts $NetworkerDeployedServer_hosts"