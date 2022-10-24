#! /bin/bash

# package is located inside .zip from Arctic Wolf
PKG_NAME="$4"
## ex: arcticwolfagent-2020-11_02.pkg


if [ "$(whoami)" != "root" ]; then
    /bin/echo "Error: You must run this command as root"
    exit 1
fi

if [[ "$PKG_NAME" == "" ]]; then 
    /bin/echo "Error: The parameter 'Arctic Wolf .pkg Name' is blank. Please specify a value." 
    exit 1 
fi

WAITING_ROOM="/Library/Application Support/JAMF/Waiting Room/"

INSTALL_PKG="${WAITING_ROOM}${PKG_NAME}"

echo "Install Package"
echo "${INSTALL_PKG}"

if [ ! -f "${INSTALL_PKG}" ]; then
    /bin/echo "Error: ${INSTALL_PKG} does not exist, exiting"
    exit 1
fi

#if not then install Arctic Wolf
## create registration token
echo '{"customerUuid":"eb915068-77b8-48cf-b18a-758057b9a1e1","registerDns":"prod-scout-reg.rootsoc.com"}' > "${WAITING_ROOM}customer.json"

END
chmod -R 777 "${WAITING_ROOM}customer.json"
/usr/sbin/installer -pkg "${INSTALL_PKG}" -target /
#clean up registration token
sleep 10
rm "${WAITING_ROOM}customer.json"

#Clean up the installer
rm "${INSTALL_PKG}"

exit 0