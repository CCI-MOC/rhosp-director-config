#!/bin/sh
#
# This file is generated with Ansible. Any changes made here will be
# lost.

export MOC_ENVIRONMENT={{ moc_environment }}
export UNDERCLOUD_IP={{ undercloud_ip | ipaddr(query="address") }}

export ControllerDeployedServer_hosts="
{% for host in groups.controller|hostname_sort(hostvars) %}
{{host}}
{% endfor %}
"
export ComputeDeployedServer_hosts="
{% for host in groups.compute|hostname_sort(hostvars) %}
{{host}}
{% endfor %}
"
export NetworkerDeployedServer_hosts="
{% for host in groups.network|hostname_sort(hostvars) %}
{{host}}
{% endfor %}
"

export OVERCLOUD_ROLES="ControllerDeployedServer ComputeDeployedServer NetworkerDeployedServer"
export OVERCLOUD_HOSTS="$ControllerDeployedServer_hosts $ComputeDeployedServer_hosts $NetworkerDeployedServer_hosts"
