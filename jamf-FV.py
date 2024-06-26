#!/Library/ManagedFrameworks/Python/Python3.framework/Versions/Current/bin/python3
import requests
from local_credentials import jamf_user, jamf_password, jamf_hostname
import csv
import json
import datetime

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
    url = jamf_hostname + "/JSSResource/computers"
    headers = {'Accept': 'application/json', 'Authorization': 'Bearer ' + token}
    response = requests.request("GET", url, headers=headers)
    return response

def getAppData(token, computers):
    headers = {'Accept': 'application/json', 'Authorization': 'Bearer ' + token}
    days = 90
    start_date = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime("%Y-%m-%d")
    end_date = datetime.datetime.now().strftime("%Y-%m-%d")
    totalUsage = {}
    for i in computers:
        id = i["computer"]["id"]
        url = jamf_hostname + f"/JSSResource/computerapplicationusage/id/{id}/{start_date}_{end_date}"
        response = requests.request("GET", url, headers=headers)
        totalUsage.update({"ID": id, "usage": response[0]["usage"]["apps"]})
    print (totalUsage)

def main():
    token = get_uapi_token()
    computers = getComputers(token)
    usage = getAppData(token, computers)

main()