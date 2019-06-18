import subprocess
import idaapi
COMMUNICATION_MANAGER_WINDOW_ID = -1
INTEGRATOR_WINDOW_ID = -1
PAUSE_HOOK = True
def start_communication_manager():
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    print " ".join(["python", "{0}\communication_manager.py".format(idaapi.idadir("plugins")), "0", "1", str(INTEGRATOR_WINDOW_ID), str(COMMUNICATION_MANAGER_WINDOW_ID)])
    subprocess.Popen(["python", "{0}\communication_manager.py".format(idaapi.idadir("plugins")), "0", "1", str(INTEGRATOR_WINDOW_ID), str(COMMUNICATION_MANAGER_WINDOW_ID)])