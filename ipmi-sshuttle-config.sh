#!/bin/sh

# Set up access to internal networks

exec sshuttle -D -r kzn-proxy 10.0.{3,5,15,19,17}.0/24
