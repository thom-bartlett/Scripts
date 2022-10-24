#!/Library/ManagedFrameworks/Python/Python3.framework/Versions/Current/bin/python3
import subprocess

def run_cmd(cmd):
    """Run the cmd"""
    run = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, err = run.communicate()
    if err:
        print(err.decode("utf-8"))
    return output, err

def logoutNow():
    '''Uses oscascript to run an AppleScript
    to tell loginwindow to logout.
    Ugly, but it works.'''

    script = """
tell application "System Events"
	log out
end tell
"""
    cmd = ['/usr/bin/osascript', '-e', script]
    _ = run_cmd(cmd)

logoutNow()