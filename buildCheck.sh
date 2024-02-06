#!/bin/bash

# Path to the .applesetupdone file
file="/var/db/.applesetupdone"

# Check if the file exists
if [ -f "$file" ]; then
    # Get the last modification date of the file
    modDate=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M:%S" "$file")
    echo "<result>$modDate</result>"
else
    echo "<result>File not found</result>"
fi