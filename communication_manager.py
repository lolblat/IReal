#import jwt
import win32con
import win32api
import win32gui
import json
import argparse
from Queue import Queue
import requests
from threading import Thread, Timer
from constants import * 

SECRECT_KEY = "RkK1EM4xHRUOfYBXvrw4"
THREAD_ARRAY = []
ID_OF_INSTANCE = -1
WINDOW_HANDLER = -1
PROJECT_ID = -1

def create_hidden_window():
	message_map = {win32con.WM_COPYDATA: message_handler}

	window_class = win32gui.WNDCLASS()
	window_class.lpfnWndProc = message_map
	window_class.lpszClassName = "Communication"
	class_atom = win32gui.RegisterClass(window_class)
	window_handler = win32gui.CreateWindow(class_atom, "Communication manager", 0, 0, 0, 0, 0, 0, 0, 0, None)
	print window_handler
	if not window_handler:
		raise Exception("Cannot create hidded window!")
	return window_handler

def insert_to_registery(window_handle):
	try:
		key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, SUBMODULE_KEY, 0, win32con.KEY_ALL_ACCESS)
	except Exception:
		key = win32api.RegCreateKeyEx(win32con.HKEY_CURRENT_USER, SUBMODULE_KEY, win32con.KEY_ALL_ACCESS, None, winnt.REG_OPTION_NON_VOLATILE, None)[0]
	win32api.RegSetValueEx(key, str(ID_OF_INSTANCE), 0, win32con.REG_SZ, str(window_handle))
	

def remove_key_from_reg():
	key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, SUBMODULE_KEY, 0, win32con.KEY_ALL_ACCESS)
	if key:
		win32api.RegDeleteValue(key, str(ID_OF_INSTANCE))

def message_handler(window_handler, msg, wParam, lParam): 
	print wParam
	if wParam == SEND_DATA_TO_SERVER: #TODO send to server
		copy_data = ctypes.cast(lParam, PCOPYDATASTRUCT)
		data_size = copy_data.contents.cbData
		data_pointer = copy_data.contents.lpData
		print ctypes.string_at(data_pointer, data_size)
	elif wParam == KILL_COMMUNICATION_MANAGER_MESSAGE_ID:
		kill()

def pull_from_server(user_token, project_id, integrator_window_key):
	params = {"user-token": user_token, "last-update": 0}
	#req = requests.get("{0}{1}".format(BASE_URL, GET_PROJECT_CHANGES_PATH.format(project_id)), params=params, timeout=2)
	#data = req.content
	#try:
#		data_parsed = json.loads(data)	
#	except ValueError:
#		return -1
	
#	new_symbols = data_parsed["symbols"]
#	window_handler_of_integrator = get_window_handler_by_id(integrator_window_key)
#	for symbol in new_symbols:
#		send_data_to_window(window_handler_of_integrator, SEND_DATA_TO_IDA, json.dumps(symbol))
		

def remove_done_threads():
	global THREAD_ARRAY
	tmp_array = []
	for t in THREAD_ARRAY:
		if t.isAlive():
			tmp_array.append(t)
	THREAD_ARRAY = tmp_array

def pulling(user_token, project_id, integrator_window_key):
	global THREAD_ARRAY
	def call_to_pull(user_token, project_id, integrator_window_key):
		pulling(user_token, project_id, integrator_window_key)
		pull_from_server(user_token, project_id, integrator_window_key)
	timer_thread = Timer(3, call_to_pull, args=(user_token, project_id, integrator_window_key,  ))
	timer_thread.start()
	remove_done_threads()
	THREAD_ARRAY.append(timer_thread)

def keep_alive_op():
	global THREAD_ARRAY
	def keep_alive():
		keep_alive_op()
	keep_alive_thread = Timer(0.01, keep_alive)
	keep_alive_thread.start()
	remove_done_threads()
	THREAD_ARRAY.append(keep_alive_thread)

def parse_args():
	parser = argparse.ArgumentParser(description="Puller for the IDA Plugin IReal")
	parser.add_argument("token", type=str)
	parser.add_argument("project_id", type=str)
	parser.add_argument("integrator_window_key", type=str)
	parser.add_argument("communication_manager_id", type=str)
	args  = parser.parse_args()
	return (args.token, args.project_id, args.integrator_window_key, args.communication_manager_id)

def main(user_token, project_id, integrator_window_key, communication_manager_id):
	global THREAD_ARRAY, WINDOW_HANDLER, ID_OF_INSTANCE, SECRECT_KEY, PROJECT_ID
	ID_OF_INSTANCE = communication_manager_id
	WINDOW_HANDLER = create_hidden_window()
	SECRECT_KEY = user_token
	PROJECT_ID = project_id
	insert_to_registery(WINDOW_HANDLER)
	pulling(user_token, project_id, integrator_window_key)
	keep_alive_op()
	win32gui.PumpMessages()

def kill():
	remove_key_from_reg()
	for thread in THREAD_ARRAY:
		thread.cancel()
	exit(0)

if __name__ == "__main__":
	user_token , project_id, integrator_window_key, communication_manager_id = parse_args()
	main(user_token, project_id, integrator_window_key, communication_manager_id)