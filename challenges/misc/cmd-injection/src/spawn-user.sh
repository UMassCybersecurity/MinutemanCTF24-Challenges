#!/bin/bash

USERNAME=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 16)
PASSWORD=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 32)

echo "[INFO] Creating user: $USERNAME"

useradd -m $USERNAME
echo "$USERNAME:$PASSWORD" | chpasswd

echo "[INFO] Spawned user!"
su - $USERNAME -s /ctf/main.py

echo "[INFO] Cleaning up user"
userdel -rf $USERNAME

echo "[INFO] User deleted!"
exit 0