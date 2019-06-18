import os
import win32api
import win32con
import struct
from array import array
import ctypes
import ctypes.wintypes
import pywintypes
import sys

BASE_URL = "https://our-amazon-web.com/"
LOGIN_PATH = "api/users/tokens"
GET_PROJECT_CHANGES_PATH = "api/projects/{0}/changes"
PUSH_DATA_TO_PROJECT  = "api/projects/{0}/push"
APPDATA_FOLDER = os.getenv("APPDATA")
SUBMODULE_KEY = "Software\\Hex-Rays\\IDA\\IPC\\Handler"

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

KILL_COMMUNICATION_MANAGER_MESSAGE_ID = 1338
SEND_DATA_TO_IDA  = 1337
SEND_DATA_TO_SERVER = 1339


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
