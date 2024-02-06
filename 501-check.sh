#!/bin/bash

# Get the UID of the user ladmin
uid=$(id -u ladmin 2>/dev/null)

# Check if the UID is 501 and output result for Jamf Pro
if [ "$uid" == "501" ]; then
    echo "<result>True</result>"
else
    echo "<result>False</result>"
fi