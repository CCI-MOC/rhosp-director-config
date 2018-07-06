#!/bin/sh

# source ~/.stackrc whenever we log in
if ! grep -q stackrc $HOME/.bashrc; then
cat >> $HOME/.bashrc <<'EOF'
if [ -f $HOME/stackrc ]; then
        . $HOME/stackrc
fi
EOF
fi

# avoid connection errors after re-deploying the overcloud servers
if ! [ -f $HOME/.ssh/config ]; then
cat > $HOME/.ssh/config <<EOF
Host *
UserKnownHostsFile /dev/null
StrictHostkeyChecking false
EOF

chmod 600 $HOME/.ssh/config
fi
