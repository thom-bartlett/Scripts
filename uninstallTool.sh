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

scriptVersion="0.0.10"
scriptLog="/var/tmp/org.wpromote.log"
export PATH=/usr/bin:/bin:/usr/sbin:/sbin
loggedInUser=$( echo "show State:/Users/ConsoleUser" | scutil | awk '/Name :/ { print $3 }' )
osVersion=$( sw_vers -productVersion )
osMajorVersion=$( echo "${osVersion}" | awk -F '.' '{print $1}' )
dialogBinary="/usr/local/bin/dialog"
dialogMessageLog=$( mktemp /var/tmp/dialogWelcomeLog.XXX )
if [[ -n ${4} ]]; then titleoption="--title"; title="${4}"; fi
if [[ -n ${5} ]]; then messageoption="--message"; message="${5}"; fi
if [[ -n ${6} ]]; then iconoption="--icon"; icon="${6}"; fi
if [[ -n ${7} ]]; then button1option="--button1text"; button1text="${7}"; fi
if [[ -n ${8} ]]; then button2option="--button2text"; button2text="${8}"; fi
if [[ -n ${9} ]]; then infobuttonoption="--infobuttontext"; infobuttontext="${9}"; fi
extraflags="${10}"


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

    updateScriptLog "Goodbye!"
    exit "${1}"

}

####################################################################################################
#
# Program
#
####################################################################################################

# Create a newline-separated string for the dropdown list
dropdownList=$(find /Applications -name "*.app" -maxdepth 3 | awk '{gsub("/Applications/", ""); printf "--checkbox '\''%s'\'' ", $0}')
echo "$dropdownList"

# Split the string into an array using comma as delimiter
#IFS=', ' read -r -a app_array <<< "$dropdownList"
#echo "${app_array[@]}"

# Initialize an empty string to hold the final JSON-like output
#json_output=()

# Loop through each app in the array
#for app in "${app_array[@]}"
#do
    # Trim leading and trailing whitespace from the app name
    #trimmed_app=$(echo "$app" | xargs)
 #   echo "$app"
 #   json_output+=("--checkbox \"$app\"")
#done

# Output the JSON-like array
#echo "${json_output[@]}"

# extra commands for display
extraflags="--width 700 --height 350 --moveable --titlefont size=26 --messagefont size=13 --iconsize 300"

titleoption="--title"
title="App Removal Tool"

messageoption="--message"
message="### This will delete an app from your Applications folder. \n\n It may not support apps with complex uninstallations such as Cisco AnyConnect or Crowdstrike."

button1option="--button1text"
button1text="Remove"

button2option="--button2text"
button2text="Cancel"

iconoption="--icon"
icon="https://github.com/unfo33/Public-scripts/blob/main/Wpromote_Logomark.png?raw=true"

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Display Message: Dialog
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

test='{
  "checkbox" : [
	  {"label" : "Option 1", "checked" : true, "disabled" : true },
	  {"label" : "Option 2", "checked" : true },
	  {"label" : "Option 3", "checked" : false },
	  {"label" : "Option 4", "checked" : true, "disabled" : true },
	  {"label" : "Option 5", "checked" : false },
	  {"label" : "Option 6", "checked" : true }
	]
}'

updateScriptLog "Title: ${title}"
updateScriptLog "Message: ${message}"
updateScriptLog "Extra Flags: ${extraflags}"

# shellcheck disable=SC2086
command=$(${dialogBinary} \
    ${titleoption} "${title}" \
    ${messageoption} "${message}" \
    ${iconoption} "${icon}" \
    ${button1option} "${button1text}" \
    ${button2option} "${button2text}" \
    ${infobuttonoption} "${infobuttontext}" \
    --big \
    --infobuttonaction "https://servicenow.company.com/support?id=kb_article_view&sysparm_article=${infobuttontext}" \
    --messagefont "size=14" \
    --commandfile "$dialogMessageLog}" \
    --checkboxstyle switch \
    --jsonstring "$test" \
    ${extraflags})

returncode=$?
updateScriptLog "Return Code: ${returncode}"

case ${returncode} in

    0)  ## Process exit code 0 scenario here
        echo "${loggedInUser} clicked ${button1text}"
        updateScriptLog "${loggedInUser} clicked ${button1text};"
        updateScriptLog "${command}"
        cleanResult=$(echo "$command" | grep '"SelectedOption"' | sed -n 's/.*: "\(.*\)"/\1/p')
        updateScriptLog "${loggedInUser} selected ${cleanResult}"
        if [[ -n "${cleanResult}" ]]; then
            sudo rm -rf "/Applications/${cleanResult}"
        else
            updateScriptLog "No applications was selected"
        fi
        quitScript "0"
        ;;

    2)  ## Process exit code 2 scenario here
        echo "${loggedInUser} clicked ${button2text}"
        updateScriptLog "${loggedInUser} clicked ${button2text};"
        quitScript "0"
        ;;

    3)  ## Process exit code 3 scenario here
        echo "${loggedInUser} clicked ${infobuttontext}"
        updateScriptLog "${loggedInUser} clicked ${infobuttontext};"
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