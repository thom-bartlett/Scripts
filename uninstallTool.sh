#!/bin/bash

####################################################################################################
#
# Created by Tom Bartlett
# Based off:
#   Display Message via swiftDialog
#   Purpose: Displays an end-user message via swiftDialog
#   See: https://snelson.us/2023/03/display-message-0-0-7-via-swiftdialog/
#
####################################################################################################

####################################################################################################
#
# Variables
#
####################################################################################################

scriptVersion="1.0.0"
scriptLog="/var/tmp/org.wpromote.log"
export PATH=/usr/bin:/bin:/usr/sbin:/sbin
loggedInUser=$( echo "show State:/Users/ConsoleUser" | scutil | awk '/Name :/ { print $3 }' )
osVersion=$( sw_vers -productVersion )
osMajorVersion=$( echo "${osVersion}" | awk -F '.' '{print $1}' )
dialogBinary="/usr/local/bin/dialog"
dialogMessageLog=$( mktemp /var/tmp/dialogWelcomeLog.XXX )
dialogHeader="https://github.com/unfo33/Public-scripts/blob/main/Wpromote_Logomark.png?raw=true"
quitMessage="Congratulations, your apps have been removed successfully!"


####################################################################################################
#
# Pre-flight Checks
#
####################################################################################################

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Pre-flight Check: Client-side Logging
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

if [[ ! -f "${scriptLog}" ]]; then
    touch "${scriptLog}"
fi


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Pre-flight Check: Client-side Script Logging Function
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

function updateScriptLog() {
    echo -e "$( date +%Y-%m-%d\ %H:%M:%S ) - ${1}" | tee -a "${scriptLog}"
}


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Pre-flight Check: Logging Preamble
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

updateScriptLog "\n\n###\n# Display Message via swiftDialog (${scriptVersion})\n###\n"
updateScriptLog "PRE-FLIGHT CHECK: Initiating …"



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Pre-flight Check: Validate Operating System
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

if [[ "${osMajorVersion}" -ge 11 ]] ; then
    updateScriptLog "PRE-FLIGHT CHECK: macOS ${osMajorVersion} installed; proceeding ..."
else
    updateScriptLog "PRE-FLIGHT CHECK: macOS ${osVersion} installed; exiting."
    osascript -e 'display dialog "Display Message via swiftDialog ('"${scriptVersion}"')\rrmacOS '"${osVersion}"' installed; macOS Big Sur 11\r(or later) required" buttons {"OK"} with icon caution with title "Display Message via swiftDialog: Error"'
    exit 1
fi

# Ensure we have latest version. Installomator is packaged with this tool.
updateScriptLog "Updating swiftdialog"
/usr/local/Installomator/Installomator.sh swiftdialog

####################################################################################################
#
# Functions
#
####################################################################################################

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Quit Script (thanks, @bartreadon!)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

function quitScript() {

    updateScriptLog "Quitting …"
    echo "quit:" >> "${dialogMessageLog}"

    sleep 1
    updateScriptLog "Exiting …"

    # Remove dialogMessageLog
    if [[ -f ${dialogMessageLog} ]]; then
        updateScriptLog "Removing ${dialogMessageLog} …"
        rm "${dialogMessageLog}"
    fi

    rm /tmp/tmpDialogFile*

    updateScriptLog "Goodbye!"
    exit "${1}"

}

####################################################################################################
#
# Program
#
####################################################################################################

#Create a tmp file to hold our dialog options
tmpDialogFile1=$(mktemp /tmp/tmpDialogFile1.XXXXXX)

#Set permissions on temp files. 
#This is necessary if the script is running as root, since dialog always runs "asuser" if using /usr/local/bin/dialog
chmod 644 "$tmpDialogFile1"

# Create list of apps formatted as JSON
dropdownList=$(find /Applications -name "*.app" -maxdepth 3 | awk 'BEGIN{print "["; sep=""}{gsub("/Applications/", ""); printf "%s{\"label\": \"%s\"}", sep, $0; sep=", "}END{print "]"}')

message="### This will delete an app from your Applications folder. \n\n It may not support apps with complex uninstallations such as Cisco AnyConnect or Crowdstrike."
title="App Removal Tool"

##Create JSON file
#https://github.com/bartreardon/swiftDialog/wiki/Using-JSON-to-specify-Dialog-options
cat > "$tmpDialogFile1" <<ADDTEXT
{
    "height" : "450",
    "width" : "900",
    "titlefont" : "size=26",
    "messagefont" : "size=13",
    "iconsize" : 300,
    "icon" : "https://github.com/unfo33/Public-scripts/blob/main/Wpromote_Logomark.png?raw=true",
	"title" : "$title",
	"message" : "$message",
    "button1text" : "Remove",
	"button2text" : "Cancel",
    "checkboxstyle" : {"style" : "switch", "size" : "small"}, 
	"checkbox" : $dropdownList
}
ADDTEXT

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Display Message: Dialog
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

updateScriptLog "Title: ${title}"
updateScriptLog "Message: ${message}"

command=$(${dialogBinary} --jsonfile "$tmpDialogFile1")
returncode=$?
updateScriptLog "Return Code: ${returncode}"

case ${returncode} in

    0)  ## Process exit code 0 scenario here
        updateScriptLog "${loggedInUser} clicked Remove;"
        #updateScriptLog "${command}"
        # clean up the results to only include apps marked as true without extra formatting
        selectedOptions=$(echo "${command}" | grep -v '"false"' | awk -F'" : "true"' '{print $1}' | sed 's/"//g')
        # Read the list into an array
        IFS=$'\n' read -r -d '' -a appArray <<< "$selectedOptions"
        # go through apps and remove them
        for app in "${appArray[@]}"; do
            if [[ -n "${app}" ]]; then
                sudo rm -rf "/Applications/${app}"
                updateScriptLog "$app was removed."
            else
                updateScriptLog "No applications was selected"
            fi
        done
        $dialogBinary --title "App Removal Complete" --small --message "$quitMessage" --icon "$dialogHeader"
        quitScript "0"
        ;;

    2)  ## Process exit code 2 scenario here
        updateScriptLog "${loggedInUser} clicked Cancel;"
        quitScript "0"
        ;;

    3)  ## Process exit code 3 scenario here
        updateScriptLog "${loggedInUser} clicked Info;"
        ;;

    4)  ## Process exit code 4 scenario here
        echo "${loggedInUser} allowed timer to expire"
        updateScriptLog "${loggedInUser} allowed timer to expire;"
        ;;

    20) ## Process exit code 20 scenario here
        echo "${loggedInUser} had Do Not Disturb enabled"
        updateScriptLog "${loggedInUser} had Do Not Disturb enabled"
        quitScript "0"
        ;;

    *)  ## Catch all processing
        echo "Something else happened; Exit code: ${returncode}"
        updateScriptLog "Something else happened; Exit code: ${returncode};"
        quitScript "${returncode}"
        ;;

esac

updateScriptLog "End-of-line."

quitScript "0"