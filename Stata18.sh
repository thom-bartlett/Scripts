#!/bin/bash

# Set the path to the JAMF Waiting Room folder.
JAMF_WAITING_ROOM="/Library/Application Support/JAMF/Waiting Room"

# This script installs Stata18 on macOS using the JAMF Pro management tool.
# It assumes that the Stata18 disk image is located in the Waiting Room folder of JAMF Pro.

# Append a choice changes XML to include the product ID of StataBE.
echo '<array><string>StataBE</string></array>' >> mychoice.xml

# Attach the Stata18 disk image using hdiutil.
hdiutil attach "$JAMF_WAITING_ROOM/Stata18.dmg"

# Install Stata18 using the product package and the choice changes XML.
# The -target / option specifies that the package should be installed on the root volume.
installer -package /Volumes/Stata/Install\ Stata.pkg -applyChoiceChangesXML mychoice.xml -target /

# Detach the Stata18 disk image using hdiutil.
hdiutil detach /Volumes/Stata

# Remove the Stata18 disk image and its cache file from the Waiting Room folder of JAMF Pro.
rm "$JAMF_WAITING_ROOM/Stata18.dmg"
rm "$JAMF_WAITING_ROOM/Stata18.dmg.cache.xml"
