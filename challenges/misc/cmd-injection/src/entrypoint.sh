#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 <listen port>"
    exit 1
fi

LISTEN_PORT=$1

echo "[INFO] Starting SSH server on port $LISTEN_PORT"
/usr/sbin/sshd -D -p $LISTEN_PORT