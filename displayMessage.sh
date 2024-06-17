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
scriptLog="/var/tmp/org.venturewell.log"
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



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Pre-flight Check: Validate / install swiftDialog (Thanks big bunches, @acodega!)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

function dialogCheck() {

    # Get the URL of the latest PKG From the Dialog GitHub repo
    dialogURL=$(curl -L --silent --fail "https://api.github.com/repos/swiftDialog/swiftDialog/releases/latest" | awk -F '"' "/browser_download_url/ && /pkg\"/ { print \$4; exit }")

    # Expected Team ID of the downloaded PKG
    expectedDialogTeamID="PWA5E9TQ59"

    # Check for Dialog and install if not found
    if [ ! -e "/Library/Application Support/Dialog/Dialog.app" ]; then

        updateScriptLog "PRE-FLIGHT CHECK: Dialog not found. Installing..."

        # Create temporary working directory
        workDirectory=$( /usr/bin/basename "$0" )
        tempDirectory=$( /usr/bin/mktemp -d "/private/tmp/$workDirectory.XXXXXX" )

        # Download the installer package
        /usr/bin/curl --location --silent "$dialogURL" -o "$tempDirectory/Dialog.pkg"

        # Verify the download
        teamID=$(/usr/sbin/spctl -a -vv -t install "$tempDirectory/Dialog.pkg" 2>&1 | awk '/origin=/ {print $NF }' | tr -d '()')

        # Install the package if Team ID validates
        if [[ "$expectedDialogTeamID" == "$teamID" ]]; then

            /usr/sbin/installer -pkg "$tempDirectory/Dialog.pkg" -target /
            sleep 2
            dialogVersion=$( /usr/local/bin/dialog --version )
            updateScriptLog "PRE-FLIGHT CHECK: swiftDialog version ${dialogVersion} installed; proceeding..."

        else

            # Display a so-called "simple" dialog if Team ID fails to validate
            osascript -e 'display dialog "Please advise your Support Representative of the following error:\r\r• Dialog Team ID verification failed\r\r" with title "Display Message via Dialog: Error" buttons {"Close"} with icon caution'
            quitScript "1"

        fi

        # Remove the temporary working directory when done
        /bin/rm -Rf "$tempDirectory"

    else

        updateScriptLog "PRE-FLIGHT CHECK: swiftDialog version $(${dialogBinary} --version) found; proceeding..."

    fi

}

if [[ ! -e "/Library/Application Support/Dialog/Dialog.app" ]]; then
    dialogCheck
else
    updateScriptLog "PRE-FLIGHT CHECK: swiftDialog version $(${dialogBinary} --version) found; proceeding..."
fi



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

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Validate Script Parameters
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

if [[ -z "${title}" ]] || [[ -z "${message}" ]]; then

    # Create a newline-separated string for the dropdown list
    dropdownList=$(find /Applications/*.app -d 0 -exec basename {} \; |  awk '{printf "%s, ", $0}' | sed 's/, $//')

    updateScriptLog "Either Parameter 4 or Parameter 5 are NOT populated; displaying instructions …"

    extraflags="--width 825 --height 400 --moveable --titlefont size=26 --messagefont size=13 --iconsize 125"

    titleoption="--title"
    title="App Remover Tool"

    messageoption="--message"
    message="### This will delete an app from your Applications folder. \n\n It may not support apps with complex uninstallations such as Cisco AnyConnect or Crowdstrike."

    button1option="--button1text"
    button1text="Remove"

    button2option="--button2text"
    button2text="Cancel"

    dropdownOption1="--selecttitle"
    dropdownTitle="Apps"

    dropdownOption2="--selectvalues"
    dropdownValue="$dropdownList"

    iconoption="--icon"
    icon="https://github.com/unfo33/Public-scripts/blob/main/Wpromote_Logomark.png?raw=true"

else

    updateScriptLog "Both \"title\" and \"message\" Parameters are populated; proceeding ..."

fi



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Display Message: Dialog
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

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
    --infobuttonaction "https://servicenow.company.com/support?id=kb_article_view&sysparm_article=${infobuttontext}" \
    --messagefont "size=14" \
    --commandfile "$dialogMessageLog}" \
    ${dropdownOption1} "${dropdownTitle}" \
    ${dropdownOption2} "${dropdownValue}" \
    ${extraflags})

returncode=$?
updateScriptLog "Return Code: ${returncode}"

case ${returncode} in

    0)  ## Process exit code 0 scenario here
        echo "${loggedInUser} clicked ${button1text}"
        updateScriptLog "${loggedInUser} clicked ${button1text};"
        cleanResult=$(echo "$command" | grep '"SelectedOption"' | sed -n 's/.*: "\(.*\)"/\1/p')
        if [[ -n "${cleanResult}" ]]; then
            updateScriptLog "${loggedInUser} selected ${cleanResult} app"
            sudo rm -rf "/Applications/$cleanResult"
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