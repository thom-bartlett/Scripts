#!/bin/bash
# Hosts file path
HOSTS_FILE="/etc/hosts"

# Entries to add
ENTRY1="127.0.0.1 tiktok.com"
ENTRY2="127.0.0.1 www.tiktok.com"

# Function to add an entry if it does not exist
add_if_not_exists() {
    local entry=$1
    if ! grep -q "$entry" "$HOSTS_FILE"; then
        echo "$entry" | sudo tee -a "$HOSTS_FILE" > /dev/null
        echo "Entry added to $HOSTS_FILE"
    else
        echo "Entry already exists, not adding"
    fi
}

# Add entries
add_if_not_exists "$ENTRY1"
add_if_not_exists "$ENTRY2"

