#!/Library/ManagedFrameworks/Python/Python3.framework/Versions/Current/bin/python3
import requests
from local_credentials import jamf_user, jamf_password, jamf_hostname
import csv
import json

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

def main():
    token = get_uapi_token()
    with open('Addigy-Device-Dump-VentureWell2.0.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            serial = row[0]
            fv = row[1]
            if computer_check(token, serial):
                jamf_Update(token, fv, serial)
            else:
                continue

main()