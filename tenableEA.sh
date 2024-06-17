#!/bin/bash

# Path to the Nessus Agent version file
nessusAgentVersionFile="/Library/NessusAgent/run/var/nessus/agent.version"

# Check if Nessus Agent version file exists
if [ -f "$nessusAgentVersionFile" ]; then
    # Read the version from the file
    nessusAgentVersion=$(cat "$nessusAgentVersionFile")
    echo "<result>$nessusAgentVersion</result>"
else
    echo "<result>Not Installed</result>"
fi