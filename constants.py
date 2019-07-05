import os
import win32api
import win32con
import struct
from array import array
import ctypes
import ctypes.wintypes
import pywintypes
import sys
import json

BASE_URL = "http://192.168.14.7:3000/"
LOGIN_PATH = "api/users/token"
GET_PROJECT_CHANGES_PATH = "api/projects/{0}/changes"
PUSH_DATA_TO_PROJECT  = "api/projects/{0}/push"
LIST_USER_PROJECT = "/api/users/{0}/projects"
START_SESSION = "/api/projects/{0}/session/start"
END_SESSION = "/api/projects/{0}/session/end"
PROJECT_DATA_FILE = "{0}\\IDAHub\\projects.dat".format(os.getenv("APPDATA"))
SUBMODULE_KEY = "Software\\Hex-Rays\\IDA\\IPC\\Handler"
SERVER_PUBLIC_KEY_PATH = "{0}\\IDAHub\\key.pub".format(os.getenv("APPDATA"))
SERVER_PUBLIC_KEY = ""
with open(SERVER_PUBLIC_KEY_PATH, "r") as f:
	SERVER_PUBLIC_KEY = f.read()

context64bit = sys.maxsize > 2**32
if context64bit:
  class COPYDATASTRUCT(ctypes.Structure):
	_fields_ = [('dwData', ctypes.c_ulonglong),
	  ('cbData', ctypes.wintypes.DWORD),
	  ('lpData', ctypes.c_void_p)]
else:
  class COPYDATASTRUCT(ctypes.Structure):
	_fields_ = [('dwData', ctypes.wintypes.DWORD),
	  ('cbData', ctypes.wintypes.DWORD),
	  ('lpData', ctypes.c_void_p)]

PCOPYDATASTRUCT = ctypes.POINTER(COPYDATASTRUCT)
def get_window_handler_by_id(window_id):
	key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, SUBMODULE_KEY, 0, win32con.KEY_ALL_ACCESS)
	value = win32api.RegQueryValueEx(key, str(window_id))[0]
	return value

def send_data_to_window(window_handler, message_type, data):
	if data:
		buf = ctypes.create_string_buffer(data)
		cds = COPYDATASTRUCT()
		cds.dwData = 1337
		cds.cbData = buf._length_
		cds.lpData = ctypes.cast(buf, ctypes.c_void_p)
	else:
		cds = '1'
	win32api.SendMessage(int(window_handler), win32con.WM_COPYDATA, int(message_type), cds)


## Create path for the config file
def create_config_file():
	if not os.path.exists(PROJECT_DATA_FILE):
		try:
			os.makedirs(os.path.dirname(PROJECT_DATA_FILE))
		except OSError as err:
			pass
		with open(PROJECT_DATA_FILE, 'w') as f:
			f.write(json.dumps({}))
	
## Messages id
SEND_DATA_TO_IDA  = 1337
KILL_COMMUNICATION_MANAGER_MESSAGE_ID = 1338
SEND_DATA_TO_SERVER = 1339

#Data: {"project-id": <project-id>}
CHANGE_PROJECT_ID = 1400

#Data: {"username": <username>, "id": <userid>, "token": <token>}
CHANGE_USER = 1401

## Events id.

CHANGE_FUNCTION_NAME_ID = 1
CHANGE_GLOBAL_VARIABLE_NAME_ID = 2
CHANGE_LABEL_NAME_ID = 3
SET_COMMENT_ID = 4
CHANGE_TYPE_ID = 5
NEW_FUNCTION_ID = 6
UNDEFINE_DATA_ID = 7
CHANGE_FUNCTION_START_ID = 8
CHANGE_FUNCTION_END_ID = 9
CREATE_STRUCT_ID = 10
CREATE_STRUCT_VARIABLE_ID = 11
DELETE_STRUCT_VARIABLE_ID = 12
CHANGE_STRUCT_ITEM_TYPE_ID = 13
DELETE_STRUCT_ID = 14
CHANGE_STRUCT_NAME_ID = 15
CREATE_ENUM_ID = 16
CREATE_ENUM_ITEM_ID = 17
CHANGE_ENUM_ITED_ID = 18
DELETE_ENUM_ID = 19
CHANGE_ENUM_NAME_ID = 20
CHANGE_FUNCTION_HEADER_ID = 21
IDA_CURSOR_CHANGE_ID = 22
EXIT_FROM_IDA_ID = 23
START_IDA_ID = 24
CHANGE_STRUCT_MEMBER_NAME_ID = 25
DELETE_ENUM_MEMBER_ID = 26


## Settings
PULLING_TIME = 1
KEEP_ALIVE_TIME = 0.01