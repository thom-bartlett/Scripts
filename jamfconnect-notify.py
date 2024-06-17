#!/Library/ManagedFrameworks/Python/Python3.framework/Versions/Current/bin/python3
import os
import json
import subprocess
from Foundation import NSLog
import sys

class DialogAlert:
    def __init__(self, message):
        # set the default look of the alert
        self.message = message
        self.content_dict = {
            "alignment": "left",
            "button1text": "Install and Logout",
            "bannerimage": "https://github.com/unfo33/venturewell-image/blob/main/Sync%20macOS%20Login%20with%20Okta.jpg?raw=true",
            "message": message,
            "icon": "https://github.com/unfo33/venturewell-image/blob/main/VentureWell_logo_mark%20(2).png?raw=true",
            "messagefont": "size=16",
            "width": "800",
            "height": "400",
            "title": "none",
            "button2text": "Defer",
            "moveable": 1,
            "timer": "900",
            "ontop": 0
        }

    def alert(self, contentDict):
        """Runs the SwiftDialog app and returns the exit code"""
        jsonString = json.dumps(contentDict)
        exit_code = subprocess.run(["/usr/local/bin/dialog", "--jsonstring", jsonString])
        return exit_code

def dialog_Check():
    dialogPath="/usr/local/bin/dialog"
    if os.path.exists(dialogPath):
        write_log("Swift Dialog Installed, proceeding")
    else:
        write_log("Swift Dialog not installed, exiting")
        sys.exit(1)

def write_log(text):
    """logger for depnotify"""
    NSLog("[mdm-switch] " + str(text))

def run_cmd(cmd):
    """Run the cmd"""
    run = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, err = run.communicate()
    if err:
        write_log(err)
        write_log(err.decode("utf-8"))
    return output, err

def main():
    # cleanup old file if it exists
    dialog_command_file = "/var/tmp/dialog.log"
    if os.path.exists(dialog_command_file):
        os.remove(dialog_command_file)
    # check if dialog is installed and latest
    dialog_Check()
    message = (f"## Please take some time to convert your macOS login to use your Okta passowrd.\n\n This process should take less than 10 minutes and will require a logout. Before you begin remember to make sure you:\n\n"
    "- Know your Mac password\n\n" 
    "- Know your Okta password (you won't be able to easily access your LastPass vault)\n\n"
    'Once complete you will use your Okta password for all future macOS logins.\n\n'
    "For more detailed instructions see: [Instructions.](https://docs.google.com/document/d/1CMeyB2Y5sbDZW37k8ZakBM-G7no_wjpR6SDexXTX8zA/edit?usp=sharing)")
    dialog = DialogAlert(message)
    run_Main = dialog.alert(dialog.content_dict)
    if run_Main.returncode == 2:
        write_log ("deferred")
    else:
        run_cmd(["jamf", "policy", "-event", "jamfconnect"])

main()