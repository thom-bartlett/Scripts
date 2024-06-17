#!/bin/bash

# This script searches for a specific file or directory across predefined paths, displays its name, and then deletes it.
# Error output is suppressed by redirecting it to /dev/null.

# Define the search paths - below are the 3 main locations - uncomment or comment what you want - can also paste a specific path if you have it
SEARCH_PATHS=(
    "/System/Volumes/Data/Users"
    #"/System/Volumes/Data/Applications"
    #"/System/Volumes/Data/Library"
)

# Enter the name of the file your looking for
SEARCH_NAME="Google Chrome.app"

if [[ -z "$SEARCH_NAME" ]]; then
    echo "Usage: $0 [file-or-directory-name]"
    exit 1
fi

for LOCATION in "${SEARCH_PATHS[@]}"
do
    echo "Searching in $LOCATION..."
    # The -iname option makes the search case insensitive
    # The first -exec echoes the file or directory name
    # The second -exec rm {} + deletes the file or directory
    # Errors are redirected to /dev/null to avoid clutter
    find "$LOCATION" -iname "$SEARCH_NAME" -exec echo "Deleting: {}" \; -exec rm -rf {} + 2>/dev/null
done

echo "Deletion complete for items named $SEARCH_NAME in the predefined paths"
