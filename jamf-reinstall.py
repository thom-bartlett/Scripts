#!/Library/ManagedFrameworks/Python/Python3.framework/Versions/Current/bin/python3
import requests
import json
from local_credentials import jamf_user, jamf_password, jamf_hostname

def get_uapi_token():
    jamf_test_url = jamf_hostname + "/api/v1/auth/token"
    headers = {'Accept': 'application/json'}
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

def reinstall():
    token = get_uapi_token()

    url = "https://venturewell.jamfcloud.com/api/v1/jamf-management-framework/redeploy/131"

    headers = {'Accept': 'application/json', 'Authorization': 'Bearer ' + token}

    response = requests.post(url, headers=headers)

    print(response.text)

def update():
    url = "https://venturewell.jamfcloud.com/api/v1/macos-managed-software-updates/send-updates"
    token = get_uapi_token()
    payload = {
        "deviceIds": ["19"],
        "skipVersionVerification": False,
        "applyMajorUpdate": False,
        "forceRestart": False,
        "updateAction": "DOWNLOAD_ONLY"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        'Authorization': 'Bearer ' + token
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)

def get_Policy():
    token = get_uapi_token()
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        'Authorization': 'Bearer ' + token
    }
    url = "https://venturewell.jamfcloud.com/JSSResource/policies"
    response = requests.get(url, headers=headers)
    responsejson = response.json()
    ids = []
    for i in responsejson["policies"]:
        ids.append(i["id"])
    
    
    icons = {}
    for i in ids:
        url = f"https://venturewell.jamfcloud.com/JSSResource/policies/id/{i}/subset/SelfService"
        response = requests.get(url, headers=headers)
        responsejson = response.json()
        if responsejson["policy"]["self_service"]["use_for_self_service"]:
            if "uri" in responsejson["policy"]["self_service"]["self_service_icon"].keys():
                icons[responsejson["policy"]["self_service"]["self_service_display_name"]] = responsejson["policy"]["self_service"]["self_service_icon"]["uri"]
    iconlist = json.dumps(icons)
    print (iconlist)

get_Policy()

