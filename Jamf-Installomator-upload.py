#!/Library/ManagedFrameworks/Python/Python3.framework/Versions/Current/bin/python3
import requests
from local_credentials import jamf_user, jamf_password, jamf_hostname
import datetime
import json


mylabels = ["adobecreativeclouddesktop","adobereaderdc", "adobereaderdc-update", "asana", "dedoose", "dropbox", "figma", "firefox", "githubdesktop", "googlechromepkg", "googledrive", "gotomeeting", "grammarly", "lastpass", "logioptions", "microsoftexcel", "microsoftpowerpoint", "microsoftteams", "microsoftword", "microsoftoffice365", "miro", "notion", "r", "rstudio", "rectangle", "slack", "spotify", "sublimetext", "webex", "zoom", "zotero"]
labelsFriendly = ["Adobe Creative Cloud", "Adobe Reader", "Adobe Reader Update", "Asana", "Dedoose", "Dropbox", "Figma", "Firefox", "Github Desktop", "Google Chrome", "Google Drive", "GoToMeeting", "Grammarly", "LastPass", "Logitech Options", "Microsoft Excel", "Microsoft PowerPoint", "Microsoft Teams", "Microsoft Word", "Microsoft Office", "Miro", "Notion", "R", "R Studio", "Rectangle", "Slack", "Spotify", "Sublime Text", "Webex", "Zoom", "Zotero"]
icons = [
    "https://ics.services.jamfcloud.com/icon/hash_3426de9c48e3cc36268c4536d86c9208e6c2a1b507fd5a3fce50bc632f35fa31",
    "https://ics.services.jamfcloud.com/icon/hash_f056cc84b938901039421acc04b5091e2cac723007285902ec0502df7947be91",
    "https://ics.services.jamfcloud.com/icon/hash_f056cc84b938901039421acc04b5091e2cac723007285902ec0502df7947be91",
    "https://ics.services.jamfcloud.com/icon/hash_65887f3e16ae8e8d04059cbe89d91098544e66b758571bb4ae955261039e3ae2",
    "https://ics.services.jamfcloud.com/icon/hash_cc7d1a2f2e9a76fdac17fefa21982a22ff4541912ade0ab0f92faeafe1e6b818",
    "https://ics.services.jamfcloud.com/icon/hash_2d7f152422a31b311f75581eb3d59dbd065241348905f09b7032dc21019e8c19",
    "https://ics.services.jamfcloud.com/icon/hash_e989412cb4eaf419264581ecb0a409fc6236d3acf93f81cc5603fcd085d05912",
    "https://ics.services.jamfcloud.com/icon/hash_e99d7d79f4e264493b08f7191ad87599e06b4bae155917251cfe9b1ab71c1682",
    "https://ics.services.jamfcloud.com/icon/hash_f1bd98223918a232d41f7139c7b789d06b51f2f08c80952ff955a5e48aec9670",
    "https://ics.services.jamfcloud.com/icon/hash_7b13221a96b59ceecc72b80e42719a6df7574a7c6195c9a36c27be0c1ce43ac3",
    "https://ics.services.jamfcloud.com/icon/hash_06daf9a94b41e43bc9e9d3339018769f1862bf8b0646c2795996fa01d25db7ba",
    "https://ics.services.jamfcloud.com/icon/hash_79e7c39aa12b82933b874e4bca51991fb25e339b0e4b79df840694e648c82aa4",
    "https://ics.services.jamfcloud.com/icon/hash_553b7ad4fe6f40d40e9d0a1a66b57758e00caf831356a7443d60b848ab36962e",
    "https://ics.services.jamfcloud.com/icon/hash_309a88fc89ed3e0ddadc04130ea3b34a97b43be98039fc0388e469c633d8186b",
    "https://ics.services.jamfcloud.com/icon/hash_424f7793aecd7cbf9834e449b5a410ce3606b9f5816e6dbc0816f5394bef3c06",
    "https://ics.services.jamfcloud.com/icon/hash_edf3f5381f4059dd51207b524c1e6f65f543cfac0eebd70c90c5e9b250b12116",
    "https://ics.services.jamfcloud.com/icon/hash_8063c6be5a7686b354c6e644c6a578e9bad32cfccfc8b0aa2d0ef1ec67ec09a4",
    "https://ics.services.jamfcloud.com/icon/hash_39f140659d95ac910c18538346b58cba0f59f1d192a197aba2fc2f0525dd3ad4",
    "https://ics.services.jamfcloud.com/icon/hash_285c2a74ab678e3a3ca9d355950592b8bcc0e5be5c272bcac64a81118581c970",
    "https://ics.services.jamfcloud.com/icon/hash_260dabede6abdf09a8d2fa254a66f772c029dd07a829d85b251906e023fdd98d",
    "https://ics.services.jamfcloud.com/icon/hash_4229ebd4203446add25e5ea4773d16970f5f88bd49524253b08369c14b69c5d8",
    "https://ics.services.jamfcloud.com/icon/hash_306408d55922f1eeb6fb5509a8c224f7b7f3ad06d602b9ac574ba449e2862efd",
    "https://ics.services.jamfcloud.com/icon/hash_90d067f8e6dbfaf6edfb60a84280bbc86dec0794775376a85f771cb1270e74be",
    "https://ics.services.jamfcloud.com/icon/hash_90d067f8e6dbfaf6edfb60a84280bbc86dec0794775376a85f771cb1270e74be",
    "https://ics.services.jamfcloud.com/icon/hash_42ce99b0514d0a5df19b1d5c3f9af8cde3bc86e986ffa6942575e2dea3152491",
    "https://ics.services.jamfcloud.com/icon/hash_395aed4c1bf684b6abd0e5587deb60aa6774dc2a525fed2d9df2b95293b72b2c",
    "https://ics.services.jamfcloud.com/icon/hash_a2f22ebda6e325c132d08f0d34292228a13b5397926dc02b8f0f76d7e48b23b5",
    "https://ics.services.jamfcloud.com/icon/hash_abe8721fbf8e36bd53b96d53a1ae94d105aab1a1cd54cc34a73c62fbed3947a4",
    "https://ics.services.jamfcloud.com/icon/hash_89856bf5aa34f516362177817144fdc14433bc265a7544978e6ff1dea34c1d8e",
    "https://ics.services.jamfcloud.com/icon/hash_2825b2da18ca491a4c06336bb36e0744b26c7584b4f44f02be5210e1b377aaa1",
    "https://ics.services.jamfcloud.com/icon/hash_0d3a3a453ad6c1cdd28be7cd24646f2990a6e442e022cb7cc4ce366cd4db8553",
]

# deprecated
def write_Script():
    for i in range(len(mylabels)):
        script = f"/usr/local/Installomator/Installomator.sh {mylabels[i]} INSTALL=force LOGO=jamf notify=SILENT"
        f = open(f"{labelsFriendly[i]}.sh", "x")
        f.write(script)
        f.close()

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


# deprecated
def script_Upload(label, friendlylabel, uapi_token):
    headers = {'Accept': 'application/json', 'Authorization': 'Bearer ' + uapi_token}
    script = f"/usr/local/Installomator/Installomator.sh {label} INSTALL=force LOGO=jamf notify=SILENT"
    today = datetime.date.today()
    payload = {
    "name": f"{friendlylabel}.sh",
    "info": "Installomator script",
    "notes": f"Created {today} by Tom Bartlett via API",
    "priority": "AFTER",
    "categoryId": "1",
    "categoryName": "scripts",
    "parameter4": "",
    "parameter5": "",
    "parameter6": "",
    "parameter7": "",
    "parameter8": "",
    "parameter9": "",
    "parameter10": "",
    "parameter11": "",
    "osRequirements": "10.14.0",
    "scriptContents": f"{script}"
    }
    url = "https://venturewell.jamfcloud.com/api/v1/scripts"

    response = requests.request("POST", url, json=payload, headers=headers)
    print(response.text)

def get_Policy(uapi_token, name):
    headers = {'Accept': "application/json", 'Authorization': 'Bearer ' + uapi_token}
    url = f"https://venturewell.jamfcloud.com/JSSResource/policies/name/{name}"
    response = requests.request("GET", url, headers=headers)
    print(f"Get Policy exit code = {response.status_code}")
    if response.status_code == 200:
        dict = json.loads(response.text)
        return dict["policy"]["general"]["id"]
    else:
        return None

# deprecated
def upload_icon(uapi_token, friendly):
    icon = f"{friendly}.png"
    headers = {"Accept": "application/json", 'Authorization': 'Bearer ' + uapi_token}
    url = "https://venturewell.jamfcloud.com/api/v1/icon/"
    files = {"file": open(f"/Users/tbartlett/Library/AutoPkg/RecipeRepos/com.github.unfo33.autopkg/Icons/{friendly}.png", "rb")}
    response = requests.post(url, files=files, headers=headers)
    dict = json.loads(response.text)
    if response.status_code == 200:
        print("icon uploaded")
        return dict["id"]
    else:
        print("Upload failed")

# deprecated
def check_icon(uapi_token, friendly):
    icon = f"{friendly}.png"
    for i in range(5, 75):
        headers = {"Accept": "application/json", 'Authorization': 'Bearer ' + uapi_token}
        url = f"https://venturewell.jamfcloud.com/api/v1/icon/{i}"
        response = requests.get(url, headers=headers)
        dict = json.loads(response.text)
        #print (dict)
        if response.status_code == 200:
            if dict["name"] == icon:
                print("icon Found")
                return dict["id"]
    return None

def create_Policy(uapi_token, friendly, label, type, icon, policy_id = 0):
    data =  f"""
    <policy>
        <general>
            <name>{friendly}</name>
            <enabled>true</enabled>
            <trigger>EVENT</trigger>
            <trigger_checkin>false</trigger_checkin>
            <trigger_enrollment_complete>false</trigger_enrollment_complete>
            <trigger_login>false</trigger_login>
            <trigger_logout>false</trigger_logout>
            <trigger_network_state_changed>false</trigger_network_state_changed>
            <trigger_startup>false</trigger_startup>
            <trigger_other>{label}</trigger_other>
            <frequency>Ongoing</frequency>
            <location_user_only>false</location_user_only>
            <target_drive>/</target_drive>
            <offline>false</offline>
            <category>
                <name>Software</name>
            </category>
            <network_limitations>
                <minimum_network_connection>No Minimum</minimum_network_connection>
                <any_ip_address>true</any_ip_address>
            </network_limitations>
            <network_requirements>Any</network_requirements>
            <site>
                <id>-1</id>
                <name>None</name>
            </site>
        </general>
        <scope>
            <all_computers>true</all_computers>
            <computers/>
            <computer_groups/>
            <buildings/>
            <departments/>
            <limit_to_users>
                <user_groups/>
            </limit_to_users>
            <limitations>
                <users/>
                <user_groups/>
                <network_segments/>
                <ibeacons/>
            </limitations>
            <exclusions>
                <computers/>
                <computer_groups/>
                <buildings/>
                <departments/>
                <users/>
                <user_groups/>
                <network_segments/>
                <ibeacons/>
            </exclusions>
        </scope>
        <self_service>
            <use_for_self_service>true</use_for_self_service>
            <self_service_display_name>{friendly} - Latest Version</self_service_display_name>
            <install_button_text>Install</install_button_text>
            <reinstall_button_text>Update/Reinstall</reinstall_button_text>
            <self_service_description>Automatically downloads and installs latest version of {friendly}. Can be used as a new install or to update existing software.</self_service_description>
            <force_users_to_view_description>false</force_users_to_view_description>
            <feature_on_main_page>false</feature_on_main_page>
            <self_service_categories>
                <category>
                    <id>2</id>
                    <display_in>true</display_in>
                    <feature_in>false</feature_in>
                </category>
            </self_service_categories>
            <notification>false</notification>
            <notification>Self Service</notification>
            <notification_subject>Install Firefox</notification_subject>
            <notification_message/>
        </self_service>
        <scripts>
            <size>3</size>
            <script>
                <id>55</id>
                <name>00_Prepare_SwiftDialog.sh</name>
                <priority>After</priority>
                <parameter4>/var/tmp/dialog.log</parameter4>
                <parameter5>Installing {friendly}...</parameter5>
                <parameter6>{icon}</parameter6>
            </script>
            <script>
                <id>54</id>
                <name>Installomator - 10.2</name>
                <priority>After</priority>
                <parameter4>{label}</parameter4>
                <parameter5>DIALOG_CMD_FILE=/var/tmp/dialog.log</parameter5>
                <parameter6>INSTALL=force</parameter6>
                <parameter7>LOGO=jamf</parameter7>
                <parameter8>NOTIFY=silent</parameter8>
            </script>
            <script>
                <id>56</id>
                <name>zz_Quit_SwiftDialog.sh</name>
                <priority>After</priority>
                <parameter4>/var/tmp/dialog.log</parameter4>
            </script>
        </scripts>
    </policy>"""

    url = f"https://venturewell.jamfcloud.com/JSSResource/policies/id/{policy_id}"
    headers = {"Accept": "application/xml", 'Content-Type': 'application/xml', 'Authorization': 'Bearer ' + uapi_token}
    response = requests.request(type, url, headers = headers, data = data)
    data = response.text
    print(data)





def main():
    # fetch Jamf Pro (ex-universal) api token
    uapi_token = get_uapi_token()
    
    #iterate through labels
    #if it exists we do to do a put
    for i in range(len(mylabels)):
        policy_id = get_Policy(uapi_token, labelsFriendly[i])
        if policy_id:
            print ("updating policy")
            create_Policy(uapi_token, labelsFriendly[i], mylabels[i], "put", icons[i], policy_id)
        # if not we need to do a post
        else:
            print("Creating policy")
            create_Policy(uapi_token, labelsFriendly[i],mylabels[i], "post", icons[i])

    # invalidating token
    print('invalidating token...')
    invalidate_uapi_token(uapi_token)


if __name__ == '__main__':
    main()