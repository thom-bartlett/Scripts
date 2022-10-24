#!/bin/sh

# This script will check the status of the SentinelOne Agent
test=$(/usr/local/bin/sentinelctl config Server Address)
if [ "$test" = "" ]; then
        echo "<result>False</result>"
else
        echo "<result>$test</result>"
fi