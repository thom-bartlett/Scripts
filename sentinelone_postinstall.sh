#! /bin/bash

## script is written by the adamcraig and sourced from https://github.com/theadamcraig/jamf-scripts/sentineone_postinstall.sh


# Unlike other sentinel installs this script will either Install on a new computer OR upgrade if sentinel is already installed. 
#I manage sentinel versions entirely from Jamf and only use one policy for both installs and upgrades.

## MAKE SURE TO ADD IN YOUR TOKEN TO REPLACE "YOURTOKENGOESHERE"

PKG_NAME="$4"
## ex: SentinelAgent_macos_v3_0_4_2657.pkg
## ex: SentinelAgent_macos_v3_2_0_2671.pkg

if [ "$(whoami)" != "root" ]; then
    /bin/echo "Error: You must run this command as root"
    exit 1
fi

if [[ "$PKG_NAME" == "" ]]; then 
    /bin/echo "Error: The parameter 'SentinelOne .pkg Name' is blank. Please specify a value." 
    exit 1 
fi

S1_BINARY="/Library/Sentinel/sentinel-agent.bundle/Contents/MacOS/sentinelctl"
WAITING_ROOM="/Library/Application Support/JAMF/Waiting Room/"

INSTALL_PKG="${WAITING_ROOM}${PKG_NAME}"
REGISTRATION="${WAITING_ROOM}com.sentinelone.registration-token"

echo "Install Package"
echo "${INSTALL_PKG}"

if [ ! -f "${INSTALL_PKG}" ]; then
    /bin/echo "Error: ${INSTALL_PKG} does not exist, exiting"
    exit 1
fi

if [[ ! -f "${REGISTRATION}" ]]; then
    /bin/echo "Registration token doesn't exist... creating..."
    echo "eyJ1cmwiOiAiaHR0cHM6Ly91c2VhMS1zMXN5LnNlbnRpbmVsb25lLm5ldCIsICJzaXRlX2tleSI6ICI4MmU4NjljZWE1NzAyMjNkIn0=" > "$REGISTRATION"
    chmod -R 777 "${WAITING_ROOM}com.sentinelone.registration-token"
fi

## if sentinelctl exists Upgrade sentinel one
if [[ -f ${S1_BINARY} ]]; then
    echo "sentinel on computer. Upgrading sentinel"
    /usr/local/bin/sentinelctl upgrade-pkg "${INSTALL_PKG}"
else
    #if not then install sentinel one
    /bin/echo "sentinel not on computer, beginning sentinel install"
    /usr/sbin/installer -pkg "${INSTALL_PKG}" -target /
fi

sleep 10

#Clean up the installer
rm "${INSTALL_PKG}"
#clean up registration token
rm "${WAITING_ROOM}com.sentinelone.registration-token"
exit 0