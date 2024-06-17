#!/bin/bash

# Get the current logged-in username
loggedInUser=$( scutil <<< "show State:/Users/ConsoleUser" | awk '/Name :/ && ! /loginwindow/ { print $3 }' )

# Check if the logged in user is "wproadmin"
if [ "$loggedInUser" = "wproadmin" ]; then
    echo "The user $loggedInUser is 'wproadmin'. Exiting."
    exit 0
fi

# Check if the user is in the admin group
if id -nG "$loggedInUser" | grep -qw admin; then
    echo "The user $loggedInUser is an admin."
    exit 1
else
    echo "The user $loggedInUser is not an admin."
    exit 0
fi