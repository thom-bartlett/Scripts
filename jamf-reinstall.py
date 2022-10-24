#!/Library/ManagedFrameworks/Python/Python3.framework/Versions/Current/bin/python3
import requests
from local_credentials import jamf_user, jamf_password, jamf_hostname

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

token = get_uapi_token()

url = "https://venturewell.jamfcloud.com/api/v1/jamf-management-framework/redeploy/85"

headers = {'Accept': 'application/json', 'Authorization': 'Bearer ' + token}

response = requests.post(url, headers=headers)

print(response.text)