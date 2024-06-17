#!/bin/sh

# Get the current primary network service
nameOfService=$(networksetup -listnetworkserviceorder | grep "Private Access" | cut -d' ' -f2-)
paStatus=$(scutil --nc status "$nameOfService" | awk '{print $1}' | head -1)

# Check if Jamf Trust VPN is active
if [[ "$paStatus" == "Disconnected" ]]; then
    # Use Jamf Trust Scheme to enable Jamf Trust VPN
    open "com.jamf.trust://?action=enable_vpn"
fi