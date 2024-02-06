#!/bin/bash

# Get the current logged-in user using scutil
current_user=$(scutil <<< "show State:/Users/ConsoleUser" | awk '/Name :/ && ! /loginwindow/ { print $3 }')

# Exit if no user is found
if [ -z "$current_user" ]; then
    echo "No current user found."
    exit 1
fi

# Check if the user is in the admin group
if id -nG "$current_user" | grep -qw admin; then
    echo "The user $current_user is an admin. Removing from admin group..."
    # Remove the user from the admin group
    dseditgroup -o edit -d "$current_user" -t user admin

    if dseditgroup -o edit -d "$current_user" -t user admin -eq 0; then
        echo "Successfully removed $current_user from the admin group."
    else
        echo "Failed to remove $current_user from the admin group."
        exit 1
    fi
else
    echo "The user $current_user is not an admin. No action taken."
    exit 0
fi
