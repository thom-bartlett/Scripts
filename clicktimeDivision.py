import os
import requests
import csv
import json
import sys

def getAirtableData():
    """Pull down relevant employee data from Airtable to create map from"""
    token = os.environ.get("AIRTABLE")
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {token}"
    }
    query = {"sort[0][field]": "Email", "cellFormat": "string", "timeZone": "UTC", "userLocale": "en-US",
        "fields": ['Email', 'Okta ID', 'Okta Status', 'First Name', 'Last Name', 'Division', 'Title', 'Department', 'Manager Email', 'Sub-Department', 'Employment Type', 'PeopleManager']}
    
    URL = "https://api.airtable.com/v0/appePY1dmnFMHaCY4/tblRs1J0Th1R43jmB"
    responseRaw = requests.get(URL, params=query, headers=headers)
    #print(responseRaw.text)
    response = responseRaw.json()
    userList = response["records"]
    offsetValue = response["offset"]
    while offsetValue:
        query["offset"] = [offsetValue]
        response = requests.get(URL, params=query, headers=headers).json()
        userList += (response["records"])
        if "offset" not in response:
            break
    return userList

def main():
    dataRaw = getAirtableData()
    divisionNames = []
    for i in dataRaw:
        if i["fields"]["PeopleManager"] == "1":
            divisionName = ""
            if "Division" in i["fields"]:
                division = i["fields"]["Division"]
                divisionName += division + " - "
            if "Department" in i["fields"]:
                department = i["fields"]["Department"]
                if department != division:
                    divisionName += department + " - "
            if "Sub-Department" in i["fields"]:
                subDepartment = i["fields"]["Sub-Department"]
                divisionName += subDepartment + " - "
            if "Title" in i["fields"]:
                title = i["fields"]["Title"]
            divisionName += title
            print (divisionName)


main()
