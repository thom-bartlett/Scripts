#!/bin/bash

# install Homebrew with Installomator
/usr/local/Installomator/Installomator.sh homebrew

# Get the currently logged-in user
loggedInUser=$( scutil <<< "show State:/Users/ConsoleUser" | awk '/Name :/ && ! /loginwindow/ { print $3 }' )

# Determine the home directory of the logged-in user
userHome=$(dscl . -read /Users/"$loggedInUser" NFSHomeDirectory | awk '{print $2}')

# Path to be added for Apple Silicon
APPLE_SILICON_PATH="export PATH=\"/opt/homebrew/bin:\$PATH\""

# Path to be added for Intel
INTEL_PATH="export PATH=\"/usr/local/bin:\$PATH\""

# File to modify
ZSHRC="${userHome}/.zshrc"

# Determine the architecture of the macOS machine
ARCH=$(uname -m)

# Function to add path to .zshrc
addPathToZshrc() {
    local pathToAdd="$1"
    # Check if the path is already in .zshrc
    if ! grep -q "$pathToAdd" "$ZSHRC"; then
        echo "Adding Homebrew path to ${ZSHRC}"
        echo "$pathToAdd" >> "$ZSHRC"
        echo "Path added. Please restart your terminal session."
    else
        echo "Homebrew path already added."
    fi
}

# Check architecture and modify .zshrc accordingly
if [[ "$ARCH" == "arm64" ]]; then
    addPathToZshrc "$APPLE_SILICON_PATH"
elif [[ "$ARCH" == "x86_64" ]]; then
    addPathToZshrc "$INTEL_PATH"
else
    echo "Unsupported architecture: $ARCH"
fi