#!/bin/bash

# Load environment variables from .env file
set -a
source .env
set +a

# Host entry to add
HOST_ENTRY="$IP $DOMAIN"

# Path to the hosts file
HOSTS_FILE="/etc/hosts"

# Check if the entry already exists
if ! grep -q "$HOST_ENTRY" "$HOSTS_FILE"; then
    # Add the entry to the hosts file
    echo "$HOST_ENTRY" | sudo tee -a "$HOSTS_FILE" > /dev/null
    echo "Entry added to hosts file."
else
    echo "Entry already exists in hosts file."
fi
