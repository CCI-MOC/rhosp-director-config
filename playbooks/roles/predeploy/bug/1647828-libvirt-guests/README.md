This is a workaround for https://bugzilla.redhat.com/show_bug.cgi?id=1647828. It will make the following changes to your system:

- Install the `containerized-libvirt-guests.service` unit, which is
  responsible for shutting down virtual guests before the nova compute
  container exits.

- Install the `virt-guests-shutdown.target` unit, which is necessary
  for correctly sequencing the activity of
  `containerized-libvirt-guests.service`. The libvirt daemon adds
  dependencies on this target to virtual guests.
