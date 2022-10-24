#! /bin/bash

# package is located inside .dmg from Stata
PKG_NAME="Install Stata.pkg"
## ex: "Install Stata.pkg"


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


## create registration token
echo "<array><string>StataBE</string></array>" > "${WAITING_ROOM}mychoice.xml"

chmod -R 777 "${WAITING_ROOM}mychoice.xml"
/usr/sbin/installer -pkg "${INSTALL_PKG}" -applyChoiceChangesXML mychoice.xml -target /
#clean up registration token
sleep 10
rm "${WAITING_ROOM}mychoice.xml"

#Clean up the installer
rm "${INSTALL_PKG}"

exit 0