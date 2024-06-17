import os
import requests
import csv
import json
import sys
import base64

def getAirtableData():
    """Pull down relevant employee data from Airtable to create map from"""
    token = os.environ.get("AIRTABLE")
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {token}"
    }
    query = {"cellFormat": "string", "timeZone": "UTC", "userLocale": "en-US", "fields": ['Name', 'Departments', 'Sub-Department (from Departments)']}
    
    URL = "https://api.airtable.com/v0/appePY1dmnFMHaCY4/tblgdSoYNGIRHPBQU"
    responseRaw = requests.get(URL, params=query, headers=headers)
    #print(responseRaw.text)
    response = responseRaw.json()
    userList = response["records"]
    return userList

def greenhouseUpdate(orgData):
    # auth data
    token = os.environ.get("ghSandbox")+":"
    encodedKEY = base64.b64encode(token.encode()).decode()
    headers = {
        "Content-Type": "application/json",
        "On-Behalf-Of": "4219726007",
        "Authorization": f"Basic {encodedKEY}"
    }
    # get existing departments
    URL = "https://harvest.greenhouse.io/v1/departments"
    response = requests.get(URL, headers=headers)
    # parse Airtable divisions
    for i in orgData:
        division = i["fields"]["Name"]
        # check if it exists already
        for department in response.json(): 
            if department["name"] == division:
                divisionID = department["id"]
            else:
                divID = False
        try:
            r = requests.post(URL, data=json.dumps({"name": division}), headers=headers)
            print (r.text)
        except:
            print (r.text)
        
        divisionID = r.json()["id"]
        departments = i["fields"]["Departments"]
        departmentList = departments.split(", ")
        if "Sub-Departments" in i["fields"]:
            subDepartment = i["fields"]["Sub-Departments"]
            subdepartmentList = subDepartment.split(", ")
        for j in departmentList: 
            if j == division:
                departmentID = divisionID
            else:
                response = requests.post(URL, data=json.dumps({"name": j, "parent_id": divisionID}), headers=headers)
                print (response.text)
                departmentID = response.json()["id"]
            if "subDepartment" in locals():
                for k in subdepartmentList:
                    response = requests.post(URL, data=json.dumps({"name": k, "parent_id": departmentID}), headers=headers)
                    print (response.text)

def main():
    dataRaw = getAirtableData()
    greenhouseUpdate(dataRaw)


main()


# get airtable info
# get existing departments
# go through Airtable divisions and check if name exists in GH already
    # if it does update to correct level
    # if not create it