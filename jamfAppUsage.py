#!/Library/ManagedFrameworks/Python/Python3.framework/Versions/Current/bin/python3
import requests
from local_credentials import jamf_user, jamf_password, jamf_hostname
import csv
import json
import datetime
from operator import itemgetter, attrgetter

def get_uapi_token():
    jamf_test_url = jamf_hostname + "/api/v1/auth/token"
    headers = {'Accept': 'application/json', }
    response = requests.post(url=jamf_test_url, headers=headers, auth=(jamf_user, jamf_password))
    response_json = response.json()
    return response_json['token']

def invalidate_uapi_token(uapi_token):
    jamf_test_url = jamf_hostname + "/api/v1/auth/invalidate-token"
    headers = {'Accept': '*/*', 'Authorization': 'Bearer ' + uapi_token}
    response = requests.post(url=jamf_test_url, headers=headers)
    if response.status_code == 204:
        print('Token invalidated!')
    else:
        print('Error invalidating token.')

def jamf_Update(uapi_token, fv, serial):
    body = f"""
    <computer>
        <extension_attributes>
            <extension_attribute>
                <id>13</id>
                <name>Addigy FileVault Keys</name>
                <type>String</type>
                <multi_value>false</multi_value>
                <value>{fv}</value>
            </extension_attribute>
        </extension_attributes>
    </computer>"""
    url = jamf_hostname + f"/JSSResource/computers/serialnumber/{serial}"
    headers = {'Accept': 'application/xml', 'Content-Type': 'application/xml', 'Authorization': 'Bearer ' + uapi_token}
    print("attempting to update Computer Object")
    response = requests.put(url, headers=headers, data=body)
    print(response.text)

def computer_check(token, serial):
    url = jamf_hostname + f"/JSSResource/computers/serialnumber/{serial}"
    headers = {'Accept': 'application/xml', 'Content-Type': 'application/xml', 'Authorization': 'Bearer ' + token}
    response = requests.request("GET", url, headers=headers)
    print(f"Get Policy exit code = {response.status_code}")
    if response.status_code == 200:
        return True
    else:
        return False

def getComputers(token):
    url = jamf_hostname + "/JSSResource/computers/subset/basic"
    headers = {'Accept': 'application/json', 'Authorization': 'Bearer ' + token}
    response = requests.request("GET", url, headers=headers)
    return response.json()

def getAppData(token, computers):
    headers = {'Accept': 'application/json', 'Authorization': 'Bearer ' + token}
    days = 90
    start_date = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime("%Y-%m-%d")
    end_date = datetime.datetime.now().strftime("%Y-%m-%d")
    totalUsage = []
    for i in computers["computers"]:
        id = i["id"]
        user = i["username"]
        url = jamf_hostname + f"/JSSResource/computerapplicationusage/id/{id}/{start_date}_{end_date}"
        response = requests.request("GET", url, headers=headers)
        responseJson = response.json()
        #print (responseJson)
        totalUsage.append({"ID": id, "user": user, "usage": responseJson["computer_application_usage"]})
    totalUsageJson = json.dumps(totalUsage)
    return totalUsageJson

def parseData(fullJson, app):
    f = open("usageData.json")
    fullJson = json.load(f)
    wordTotal = []
    pptTotal = []
    excelTotal = []
    for firstLevel in fullJson:
        #print (firstLevel)
        computerID = firstLevel["ID"]
        computerUser = firstLevel["user"]
        wordUsage = 0
        pptUsage = 0
        excelUsage = 0
        for usage in firstLevel["usage"]:
            #print (usage)
            for apps in usage["apps"]:
                #print (apps)
                if apps["name"] == "Microsoft Word.app":
                    wordUsage += apps["foreground"]
                elif apps["name"] == "Microsoft Excel.app":
                    pptUsage += apps["foreground"]
                elif apps["name"] == "Microsoft PowerPoint.app": 
                    excelUsage += apps["foreground"]
        wordUsage = round(wordUsage / 60)
        excelUsage = round(excelUsage / 60)
        pptUsage = round(pptUsage / 60)
        wordTotal.append({"ID": computerID, "User": computerUser, "Word Usage": wordUsage})
        pptTotal.append({"ID": computerID, "User": computerUser, "PPT Usage": pptUsage})
        excelTotal.append({"ID": computerID, "User": computerUser, "Excel Usage": excelUsage})
    
    wordSorted = sorted(wordTotal, key=lambda x: x["Word Usage"])
    excelSorted = sorted(excelTotal, key=lambda x: x["Excel Usage"])
    pptSorted = sorted(pptTotal, key=lambda x: x["PPT Usage"])
    filename = "wordFinal.csv"
    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["ID", "User", "Word Usage"])
        writer.writeheader()
        for i in wordSorted:
            writer.writerow(i)
    filename = "excelFinal.csv"
    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["ID", "User", "Excel Usage"])
        writer.writeheader()
        for i in excelSorted:
            writer.writerow(i)
    filename = "pptFinal.csv"
    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["ID", "User", "PPT Usage"])
        writer.writeheader()
        for i in pptSorted:
            writer.writerow(i)


def main():
    token = get_uapi_token()
    computers = getComputers(token)
    #print(computers)
    usage = getAppData(token, computers)
    with open("usageData.json", "w") as outfile:
        outfile.write(usage)

parseData("test", "Microsoft Word.app")