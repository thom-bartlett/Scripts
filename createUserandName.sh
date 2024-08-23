#!/bin/bash

# get current user
username=$( scutil <<< "show State:/Users/ConsoleUser" | awk '/Name :/ && ! /loginwindow/ { print $3 }' )

# Function to generate a random password
generate_password() {
  local password_length=16
  LC_ALL=C tr -dc 'A-Za-z0-9' < /dev/urandom | head -c $password_length
}

# Get the serial number of the computer
serialNumber=$(system_profiler SPHardwareDataType | awk '/Serial Number/{print $4}')

# Format the new computer name
newComputerName="${username}_Incyte_${serialNumber}"

# Set the new computer name
sudo scutil --set ComputerName "$newComputerName"
sudo scutil --set HostName "$newComputerName"
sudo scutil --set LocalHostName "$newComputerName"

# Generate a random password for the new admin user
adminPassword=$(generate_password)

# Create the new admin user
sudo sysadminctl -addUser IncyteITSupport -fullName "IT Support" -password "$adminPassword" -admin

# Create the new user
# sudo sysadminctl -addUser "$username" -password "$password" -admin


# Output the generated password
echo "The password for IncyteITSupport is: $adminPassword"

# Log the password to a file
echo "IncyteITSupport password: $adminPassword" | sudo tee /var/root/IncyteITSupport_password.txt > /dev/null

# Set file permissions so only root can read the password file
sudo chmod 600 /var/root/IncyteITSupport_password.txt
