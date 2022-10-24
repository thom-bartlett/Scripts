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
            "alignment": "center",
            "button1text": "Acknowledge",
            "bannerimage": "https://github.com/unfo33/venturewell-image/blob/main/macos_restart_required.jpeg?raw=true",
            "message": message,
            "messagefont": "size=16",
            "title": "none",
            "moveable": 1,
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
    # check if uptime is > 24 hours and if so report number of days, otherwise 0
    uptime_raw = run_cmd("uptime")
    uptime_hours = uptime_raw[0].split()
    if uptime_hours[3] == "day," or uptime_hours[3] == "days,":
        uptime = uptime_hours[2]
        print (uptime)
    else:
        uptime = 0
        print(uptime)
    if int(uptime) < 20:
        pass
        print("Uptime less than 20")
    else:
        message = (f"## Your Computer has not been restarted in {uptime} days.\n\n Please take some time to restart to ensure your computer receives all updates and is running optimally.\n\n"
        'After selecting "Apple menu  > Restart" if you leave "Reopen windows when logging back in." selected your windows and tabs should automatically reopen.\n\n'
        "For more information or instructions see: [Apple's Documentation](https://support.apple.com/guide/mac-help/shut-down-or-restart-your-mac-mchlp2522/12.0/mac/12.0)")
        dialog = DialogAlert(message)
        run_Main = dialog.alert(dialog.content_dict)

main()