import objc
import subprocess

from AppKit import NSWorkspace, NSRunningApplication
from Quartz import CGWindowListCopyWindowInfo, kCGNullWindowID, kCGWindowListOptionAll

from dataclasses import dataclass


@dataclass
class EVEWindow:
    pid: int
    owner: str
    title: str


def get_open_eve_windows():
    window_list = CGWindowListCopyWindowInfo(kCGWindowListOptionAll, kCGNullWindowID)

    eve_windows = []
    
    for window in window_list:
        window_title = window.get('kCGWindowName', 'Unknown')
        window_owner = window.get('kCGWindowOwnerName', 'Unknown')
        window_pid = window.get('kCGWindowOwnerPID', 0)
        if "EVE" in window_owner:
            if is_not_in_eve_window(eve_windows, window_pid):
                eve_windows.append(EVEWindow(window_pid, window_owner, window_title))
    
    return eve_windows

def focus_eve_window(pid):
    switch_to_application_space(pid)
    bring_window_to_front(pid)


# Sends the window to front/focuses it
def bring_window_to_front(pid):
    app = NSRunningApplication.runningApplicationWithProcessIdentifier_(pid)
    if app:
        app.activateWithOptions_(objc.YES)
        return True
    return False


# Switches to the virtual desktop screen of that window
def switch_to_application_space(pid):
    script = f'''
    tell application "System Events"
        set appProc to first process whose unix id is {pid}
        set frontmost of appProc to true
    end tell
    '''
    subprocess.call(['osascript', '-e', script])


# Checks if window with pid is already inside the array
def is_not_in_eve_window(eve_windows, pid):
    for window in eve_windows:
        if pid == window.pid:
            return False
    return True