#!/Library/ManagedFrameworks/Python/Python3.framework/Versions/Current/bin/python3
import requests
import json
import re

from local_credentials import snipe_token

def snipe_GetInfo():
    url = f"https://snipe.venturewell.org/api/v1/users?limit=200&offset=0&sort=created_at&order=desc&deleted=false&all=false"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {snipe_token}"
    }
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    return data

def solve(s):
   pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
   if re.match(pat,s):
      return True
   return False

def main():
    users = snipe_GetInfo()

    for user in users["rows"]:
        id = user["id"]
        print(id)
        user = user["username"]
        print(user)
        url = f"https://snipe.venturewell.org/api/v1/users/{id}"
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {snipe_token}",
            "Content-Type": "application/json"
        }
        if solve(user):
            payload = user
        else:
            payload = user+"@venturewell.org"
            payload = {"username": payload}
            # payload_Json = json.dumps(payload)
            response = requests.patch(url, json=payload, headers=headers)
            print (response)
 
main()