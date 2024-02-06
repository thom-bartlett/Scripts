import os
import asyncio
import requests
from okta.client import Client as OktaClient
import csv
import subprocess
import json
import sys
from csv_diff import load_csv, compare

def getAirtableData():
    """Pull down relevant employee data from Airtable to create map from"""
    token = os.environ.get("AIRTABLE")
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {token}"
    }
    query = {"sort[0][field]": "Email", "cellFormat": "string", "timeZone": "UTC", "userLocale": "en-US",
        "fields": ['Email', 'Okta ID', 'Okta Status', 'First Name', 'Last Name', 'Honorific Prefix', 'Honorific Suffix', 'Secondary Email', 'Mobile Phone', 'Primary Phone', 'State', 'Division', 'Manager', 'Pronoun', 'Role', 'Time Zone', 'Title', 'Department', 'Manager Email', 'Start Date', 'Legal First Name', 'Legal Last Name', 'Sub-Department', 'Employment Type'] }
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

async def getOktaData():
    token = os.environ.get("OKTA")
    config = {
        'orgUrl': 'https://venturewell.okta.com',
        'token': token
    }
    okta_client = OktaClient(config)
    # Actually call to Okta
    users, resp, err = await okta_client.list_users()
    return users

async def updateOkta(attributeKey, userChanges):
    token = os.environ.get("OKTA")
    config = {
        #'orgUrl': 'https://dev-11554259.okta.com',
        'orgUrl': 'https://venturewell.okta.com',
        'token': token
    }
    okta_client = OktaClient(config)
    with open('/Users/tbartlett/Airtable.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            if lines[0] in userChanges:
                if lines[0] == "Email":
                    pass
                else:
                    userProfile = {}
                    index = 0
                    for i in range(len(lines)):
                        if i == 1:
                            user_id = lines[1]
                        elif i == 2:
                            pass
                        else:
                            userProfile[attributeKey[index]] = lines[i]
                        index+=1
                    user_params = {'profile': userProfile}
                    #print (user_params)
                    print (f"Updating User: {lines[0]}")
                    # Actually call to Okta
                    updated_user, resp, err = await okta_client.partial_update_user(user_id, user_params)
                    print (resp, err)
    

def createCSV(data, headers, attributeKey, source):
    # initialize list
    newList = []
    # go through data and construct new list of objects to add empty strings for all the fields that didn't have data
    for user in data:
        # create new dictionary to be added to list
        newDict = {}
        index = 0
        # go through attribute keys and match them up with keys that exist in Okta data
        for value in attributeKey:
            if source == "okta":
                keys = user.profile.as_dict().keys()
            else:
                #print(user)
                keys = user["fields"].keys()
            for key in keys:
                if key == value:
                    if source == "okta":
                        newDict[headers[index]] = user.profile.as_dict()[key]
                        # print(user.profile.as_dict()[key])
                    else:
                        newDict[headers[index]] = user["fields"][key]
            if headers[index] == "Okta Status" and source == "okta":
                newDict[headers[index]] = user.status.value
            elif headers[index] == "Okta ID" and source == "okta":
                newDict[headers[index]] = user.id
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

def csvCompare(argument):
    diff = compare(
        load_csv(open("/Users/tbartlett/Okta.csv"), key="Email"),
        load_csv(open("/Users/tbartlett/Airtable.csv"), key="Email"))
    if argument == "update":
        userChanges = []
        for i in diff["changed"]:
            userChanges.append(i["key"])
        updateKey = ["email", "Okta ID", "Okta Status", "firstName", "lastName", "honorificPrefix", "honorificSuffix", "secondEmail", "mobilePhone", "primaryPhone", "state", "division", "manager", "pronoun", 'role', 'time_zone', 'vwtitle', 'custom_department', 'manageremail', 'startdate', 'legalfirst', 'legallast', 'Subdepartment', 'employment']
        loop = asyncio.get_event_loop()
        loop.run_until_complete(updateOkta(updateKey, userChanges))
    else:
        print (json.dumps(diff, indent=2))

def main():
    argument = ""
    if len(sys.argv) > 1:
        argument = sys.argv[1]
        csvCompare(argument)
    else:
        attributeKey = ["login", "Okta ID", "Okta Status", "firstName", "lastName", "honorificPrefix", "honorificSuffix", "secondEmail", "mobilePhone", "primaryPhone", "state", "division", "manager", "pronoun", 'role', 'time_zone', 'vwtitle', 'custom_department', 'manageremail', 'startdate', 'legalfirst', 'legallast', 'Subdepartment', 'employment']
        headers = ['Email', "Okta ID", "Okta Status", 'First Name', 'Last Name', 'Honorific Prefix', 'Honorific Suffix', 'Secondary Email', 'Mobile Phone', 'Primary Phone', 'State', 'Division', 'Manager', 'Pronoun', 'Role', 'Time Zone', 'Title', 'Department', 'Manager Email', 'Start Date', 'Legal First Name', 'Legal Last Name', 'Sub-Department', 'Employment Type']
        # get data and create Okta CSV
        loop = asyncio.get_event_loop()
        oktaData = loop.run_until_complete(getOktaData())
        oktaCSV = createCSV(oktaData, headers, attributeKey, "okta")
        writeCSV(oktaCSV, "okta", headers)
        # get data and creeate Airtable CSV
        airtableData = getAirtableData()
        airtableCSV = createCSV(airtableData, headers, headers, "airtable")
        writeCSV(airtableCSV, "airtable", headers)
        csvCompare(argument)

main()
