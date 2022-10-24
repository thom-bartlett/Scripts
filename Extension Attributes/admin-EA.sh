#!/usr/bin/env -i /bin/bash

# Force the script to quit if any error encountered
set -e

# Initialize array variable to hold admin usernames
list=()

# For all users with a userID above 500 (aka: not hidden) check if they are an admin, if so, AND not a known administrative service account, add to list array
for username in $(/usr/bin/dscl . list /Users UniqueID | /usr/bin/awk '$2 > 500 { print $1 }'); do
    if [[ $(/usr/bin/dsmemberutil checkmembership -U "${username}" -G admin) != *not* ]]; then
        if [[ "${username}" != 'ladmin' ]]; then
                list+=("${username}")
        fi
    fi
done

# Print all items in the list array
/bin/echo "<result>${list[@]}</result>"