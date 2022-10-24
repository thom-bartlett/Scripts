#!/bin/bash

# we need to wait for the dock to actually start
until [[ $(pgrep Dock) ]]; do
    wait
done

# Find the JAMF binary
jamfbinary="/usr/local/bin/jamf"

# Chesk to see if we have dockutil installed, install if not
if [ ! -f "/usr/local/bin/dockutil" ]; then
	echo "Installing DockUtil from JSS"
	"$jamfbinary" policy -event dockutil
	if [ ! -f "/usr/local/bin/dockutil" ]; then # Did the install work?
		echo "Unable to install DockUtil, aborting!"
		exit 1
	fi
fi
du="/usr/local/bin/dockutil"

# Get the current logged in user that we'll be modifying
user=$( scutil <<< "show State:/Users/ConsoleUser" | awk '/Name :/ && ! /loginwindow/ { print $3 }' )
echo "Running DockMaster on $user"

# Get current OS
os=$( sw_vers -ProductVersion )

added_Apps=("Slack.app" "zoom.us.app" "Asana.app" "Microsoft Word.app" "Microsoft Excel.app" "Google Chrome.app" "Self Service.app")

# Clear the default dock
echo "Removing all items from the dock"
$du --remove all --no-restart /Users/"$user"
sleep 2 # we need to give this time to work or we'll get errors with "replacing" items instead of adding them

# Check for and Install Added Apps
for  i in "${added_Apps[@]}"; do
    if [ -d "/Applications/$i" ]; then
        $du --add "/Applications/$i" --no-restart /Users/"$user"
    else :
        echo "$i not installed... skipping..."
    fi
done

# check which version of macOS for System preference name
if [[ "$os" == 13.* ]]; then
    $du --add "/System/Applications/System Settings.app" --no-restart /Users/"$user"
else :
    $du --add "/System/Applications/System Preferences.app" --no-restart /Users/"$user"
fi
# replace other system apps
$du --add "/System/Applications/Launchpad.app" --no-restart /Users/"$user"
$du --add "/System/Applications/Notes.app" --no-restart /Users/"$user"

# Restart the dock after everything is done
sleep 2
killall Dock
exit
