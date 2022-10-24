#!/bin/bash

arch=$(/usr/bin/arch)
if [ "$arch" == "arm64" ]; then
    echo "This is an arm64 Mac."
    if [[ -d "/Library/Apple/usr/libexec/oah" ]]; then
        echo "Rosetta 2 is already installed"
    else
        echo "Rosetta 2 not installed - trying"
        /usr/sbin/softwareupdate --install-rosetta --agree-to-license
        if [[ -d "/Library/Apple/usr/libexec/oah" ]]; then
            echo "Rosetta 2 is now installed"
        else
            echo "Rosetta 2 not detected"
        fi
    fi
else
    echo "This is an Intel Mac."
fi