import os
import requests
import csv
import json
import sys

def getAirtableData(type):
    """Pull down relevant employee data from Airtable to create map from"""
    token = os.environ.get("AIRTABLE")
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {token}"
    }
    if type == "sync":
        query = {"sort[0][field]": "Email", "cellFormat": "string", "timeZone": "UTC", "userLocale": "en-US",
            "fields": ['Email', 'Okta ID', 'Okta Status', 'First Name', 'Last Name', 'Honorific Prefix', 'Honorific Suffix', 'Secondary Email', 'Mobile Phone', 'Primary Phone', 'State', 'Division', 'Manager', 'Pronoun', 'Role', 'Time Zone', 'Title', 'Department', 'Manager Email', 'Start Date', 'Legal First Name', 'Legal Last Name', 'Sub-Department', 'Employment Type']}
    elif type == "map":
        query = {"sort[0][field]": "Email", "cellFormat": "string", "timeZone": "UTC", "userLocale": "en-US",
            "fields": ['Email', 'Full Name', 'Role', 'Title', 'Department', 'Manager Email', 'Sub-Department']}

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
    
def createCSV(data, headers):
    nonFullTime = ["service account", "external consultant", "non-benefits eligible staff"]
    # initialize list
    newList = []
    # go through data and construct new list of objects to add empty strings for all the fields that didn't have data
    for user in data:
        if user["fields"]["Role"] in nonFullTime:
            pass
        else:
            # create new dictionary to be added to list
            newDict = {}
            index = 0
            # go through attribute keys and match them up with keys that exist in Okta data
            for value in headers:
                keys = user["fields"].keys()
                for key in keys:
                    if key == value:
                        newDict[headers[index]] = user["fields"][key]
                        print (user["fields"][key])
                index+=1
            # add new dict to list
            newList.append(newDict)
    newList.sort(key=lambda x: x["Email"])
    return newList

def writeCSV(data, source, headers):
    if source == "okta":
        output_file_path = '/Users/tbartlett/Okta.csv'
    else:
        output_file_path = '/Users/tbartlett/Airtable.csv'
    # write data to CSV
    with open(output_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for i in data:
            writer.writerow(i)
    output_file_path

def main():
    type = sys.argv[1]
    if type == "sync":
        headers = ['Email', "Okta ID", "Okta Status", 'First Name', 'Last Name', 'Honorific Prefix', 'Honorific Suffix', 'Secondary Email', 'Mobile Phone', 'Primary Phone', 'State', 'Division', 'Manager', 'Pronoun', 'Role', 'Time Zone', 'Title', 'Department', 'Manager Email', 'Start Date', 'Legal First Name', 'Legal Last Name', 'Sub-Department', 'Employment Type']
    elif type == "map":
        headers = ['Email', 'Full Name', 'Role', 'Title', 'Department', 'Manager Email', 'Sub-Department']
    # get data and creeate Airtable CSV
    airtableData = getAirtableData(type)
    airtableCSV = createCSV(airtableData, headers)
    writeCSV(airtableCSV, "airtable", headers)

main()
