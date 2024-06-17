#!/bin/sh

token="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6Ijc0NGU1MWFjNzY4OThiZTk4ZmVlNWZjNjM3MDNiNzAwOTE1ODExOTYyZDRkZDY5YTk0NThiYmIwNjIwY2RkMzZhZjg2ZDQ2YTIzNmFkNTAxIn0.eyJhdWQiOiIxIiwianRpIjoiNzQ0ZTUxYWM3Njg5OGJlOThmZWU1ZmM2MzcwM2I3MDA5MTU4MTE5NjJkNGRkNjlhOTQ1OGJiYjA2MjBjZGQzNmFmODZkNDZhMjM2YWQ1MDEiLCJpYXQiOjE2Nzg0Nzk0MTgsIm5iZiI6MTY3ODQ3OTQxOCwiZXhwIjoxNzEwMDk4MjE4LCJzdWIiOiIxIiwic2NvcGVzIjpbXX0.aSmSAkXD06smoSRmiUMcR9-VJlkLGLuaoFsy464pTaEJC3yxB-mfh-CNiLf36R7O1lqWTPFMN5oWV-C8HmjlqdYczfbkfDDONHoSbFNTrOEFG7agNfm_DNoEofHyo_Hc3CFQzD-NfGolwE53wPWHuj3UE58QG4KAaRzT-rdILEgEC9mk6E5f_EHNswqjvdTCjgKmPGT9HFxg5swuCuLvJQhMBg8KKreR76RpU5x3t_JcE7Em8ag2IkeF1NXXzrUmzypqTKa7ksvx25NdrnYUokyl-h_bdq2drlhA9fs5eTKdT0n2q9mxE6opO1T83tmiEmh354VgoUnH0ZOD5oyNCGKb5x0nwoS6fic9Y4FWVoWmangZPKWc7_ucuXfkN-vqvu_UHDlDg0EbvlJ0DgpVamiUVcA1htXz6wKkAeqiO-uVqma8qu6hO_OkXC6-OqJ9_QIvzSKxJq7c0aDIRmc-F9T9WCz41u5lknoP0jgInOKmpRXMysKTyZDGXogenSEf9zW3zmKy3OO9Zb04yQtxLAexV7-qDFragc5xQRGu1XP3Ba9GJfyEcBCxKSyGd66gmo-JSJHzFBlw1wYifE4lZvQpGMWpkiq2xzY-ct3RJPxXrQf7q7GJ9_9-K4ycY5wUB84m-bF11768qLwnzDAGh43OsEP-MuCQqrSKn1nmcQE"
SERIAL=$(system_profiler SPHardwareDataType | grep -i Serial | grep -i system | awk '{print $NF}')

getJsonValue() {
  # $1: JSON string to parse, $2: JSON key to look up
  # $1 is passed as a command-specific environment variable so that no special
  # characters in valid JSON need to be escaped, and no code execution is
  # possible since the contents cannot be interpreted as code when retrieved
  # within JXA.
  # $2 is placed directly in the JXA code since it should not be coming from
  # user input or an arbitrary source where it could be set to intentionally
  # malicious contents.
  JSON="$1" osascript -l 'JavaScript' \
    -e 'const env = $.NSProcessInfo.processInfo.environment.objectForKey("JSON").js' \
    -e "JSON.parse(env).$2"
}

data=$(curl --location --request GET "https://snipe.venturewell.org/api/v1/hardware/byserial/$SERIAL" \
--header "Authorization: Bearer $token" \
--header 'Accept: application/json' \
--header 'Content-Type: application/json' \
--header 'Cookie: snipeit_session=q50a7MF3RFt8We5nb5gJfMfz3cDmfodiZfrYX9E4')
echo "$data"
newName=$(getJsonValue "$data" 'rows[0].name')
echo "$newName"

if [ -z "$newName" ]; then
    echo "Not in Snipe - using Serial Number"

    # Get Serial
    SERIAL=$(system_profiler SPHardwareDataType | grep -i Serial | grep -i system | awk '{print $NF}')

    # Set all the name in all the places
    scutil --set ComputerName "$SERIAL"
    scutil --set LocalHostName "$SERIAL"
    scutil --set HostName "$SERIAL"
    
else
    # Set name to value from snipe
    scutil --set ComputerName "$newName"
    scutil --set LocalHostName "$newName"
    scutil --set HostName "$newName"
fi
