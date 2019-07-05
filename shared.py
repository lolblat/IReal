import subprocess
import idaapi
COMMUNICATION_MANAGER_WINDOW_ID = -1
INTEGRATOR_WINDOW_ID = -1
PAUSE_HOOK = True
IS_COMMUNICATION_MANAGER_STARTED = False


USERNAME = ""
USERID = -1
PROJECT_ID = -1
USER_TOKEN = ""

def start_communication_manager():
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    print " ".join(["python", "{0}\communication_manager.py".format(idaapi.idadir("plugins")),  str(INTEGRATOR_WINDOW_ID), str(COMMUNICATION_MANAGER_WINDOW_ID)])
    subprocess.Popen(["python", "{0}\communication_manager.py".format(idaapi.idadir("plugins")), str(INTEGRATOR_WINDOW_ID), str(COMMUNICATION_MANAGER_WINDOW_ID)])