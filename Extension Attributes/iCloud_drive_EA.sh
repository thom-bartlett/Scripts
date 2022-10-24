#!/bin/zsh
MobileDocsCount=$(ls -l /Users/*/Library/"Mobile Documents"/ | wc -l | sed 's/ //g')
MobileDocs=$(ls -l /Users/*/Library/ | grep "Mobile Documents" | wc -l | sed 's/ //g')

if [ $MobileDocs != 0 ]; then
        if [ $MobileDocsCount -le 1 ]; then
                echo "<result>Disabled</result>"
        else
                echo "<result>Enabled</result>"
        fi
else
        echo "<result>Disabled</result>"
fi