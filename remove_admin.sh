#!/bin/bash

if [ "$4" != "" ]; then
    loggedInUser=$( scutil <<< "show State:/Users/ConsoleUser" | awk '/Name :/ && ! /loginwindow/ { print $3 }' )
else
    loggedInUser="$4"
fi

dseditgroup -o edit -d "$loggedInUser" -t user admin