import threading,subprocess
def GetDevices():
    devices = subprocess.check_output(" devices")
GetDevices()