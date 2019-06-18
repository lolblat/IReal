import idaapi
import ctypes
import win32api
import win32gui
import win32con
import winnt
import os
import struct
import constants
import shared
from all_events import *

def log(data):
	print("[Integrator] " + data)

def create_hidden_window():
	window_handler = win32gui.CreateWindow("EDIT", "Integrator window hook", 0, 0, 0, 0, 0, 0, 0, 0, None)
	if not window_handler:
		raise Exception("Cannot create hidded window!")
	win32gui.SetWindowLong(window_handler, win32con.GWL_WNDPROC, message_handler)
	return window_handler

def insert_to_registery(window_handle):
	id_of_instance = struct.unpack(">I", os.urandom(4))[0]
	try:
		key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, constants.SUBMODULE_KEY, 0, win32con.KEY_ALL_ACCESS)
	except Exception:
		key = win32api.RegCreateKeyEx(win32con.HKEY_CURRENT_USER, constants.SUBMODULE_KEY, win32con.KEY_ALL_ACCESS, None, winnt.REG_OPTION_NON_VOLATILE, None)[0]
	win32api.RegSetValueEx(key, str(id_of_instance), 0, win32con.REG_SZ, str(window_handle))
	return id_of_instance
	

def remove_key_from_reg(id_of_instance):
	key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, constants.SUBMODULE_KEY, 0, win32con.KEY_ALL_ACCESS)
	if key:
		win32api.RegDeleteValue(key, str(id_of_instance))

def message_handler(window_handler, msg, wParam, lParam):
	if wParam == constants.SEND_DATA_TO_IDA: #pass
		copy_data = ctypes.cast(lParam, constants.PCOPYDATASTRUCT)
		event_data = json.loads(ctypes.string_at(copy_data.constants.lpData))
		event_object = create_event_from_dict(event_data)
		log("Received object: " + str(event_data))
		event_object.implement()
	return True

def create_event_from_dict(json_dict):
	event_id = json_dict["id"]
	event_data = json_dict["data"]
	if event_id == constants.CHANGE_FUNCTION_NAME_ID:
		return ChangeFunctionNameEvent(event_data["value"], event_data["linear-address"])
	elif event_id == constants.CHANGE_GLOBAL_VARIABLE_NAME_ID:
		return ChangeGlobalVariableNameEvent(event_data["linear-address"], event_data["value"], event_data["label-type"])
	elif event_id == constants.CHANGE_LABEL_NAME_ID:
		return ChangeLabelNameEvent(event_data["linear-address"], event_data["value"])
	elif event_id == constants.SET_COMMENT_ID:
		return ChangeCommentEvent(event_data["linear-address"], event_data["value"], event_data["comment-type"])
	elif event_id == constants.CHANGE_TYPE_ID:
		return ChangeTypeEvent(event_data["linear-address"], event_data["variable-type"])
	elif event_id == constants.NEW_FUNCTION_ID:
		return NewFunctionEvent(event_data["linear-address-start"],event_data["linear-address-end"])
	elif event_id == constants.UNDEFINE_DATA_ID:
		return UndefineDataEvent(event_data["linear-address"])
	elif event_id == constants.CHANGE_FUNCTION_START_ID:
		return ChangeFunctionStartEvent(event_data["linear-address"], event_data["value"])
	elif event_id == constants.CHANGE_FUNCTION_END_ID:
		return ChangeFunctionEndEvent(event_data["linear-address"], event_data["value"])
	elif event_id == constants.CREATE_STRUCT_ID:
		return CreateStructEvent(event_data["name"], event_data["id"])
	elif event_id == constants.CREATE_STRUCT_VARIABLE_ID:
		return CreateStructVariableEvent(event_data["id"], event_data["offset"], event_data["variable-type"])
	elif event_id == constants.DELETE_STRUCT_VARIABLE_ID:
		return DeleteStructVariableEvent(event_data["id"], event_data["offset"])
	elif event_id == constants.DELETE_STRUCT_ID:
		return DeleteStructEvent(event_data["id"])
	elif event_id == constants.CHANGE_STRUCT_NAME_ID:
		return ChangeStructNameEvent(event_data["id"], event_data["value"])
	elif event_id == constants.CREATE_ENUM_ID:
		return CreateEnumEvent(event_data["name"], event_data["id"])
	elif event_id == constants.CREATE_ENUM_ITEM_ID:
		return CreateEnumItemEvent(event_data["id"], event_data["name"], event_data["value"])
	elif event_id == constants.DELETE_ENUM_ID:
		return DeleteEnumEvent(event_data["id"])
	elif event_id == constants.CHANGE_ENUM_NAME_ID:
		return ChangeEnumNameEvent(event_data["id"], event_data["value"])
	elif event_id == constants.CHANGE_FUNCTION_HEADER_ID:
		return ChangeFunctionHeaderEvent(event_data["linear-address"], event_data["value"])
	elif event_id == constants.IDA_CURSOR_CHANGE_ID:
		return IDACursorEvent(event_data["linear-address"])
	elif event_id == constants.EXIT_FROM_IDA_ID:
		return ExitIDBEvent()
	elif event_id == constants.START_IDA_ID:
		return StartIDAEvent()
	elif event_id == constants.CHANGE_STRUCT_MEMBER_NAME_ID:
		return ChangeStructItemEvent(event_data["id"], event_data["offset"], event_data["value"])
	elif event_id == constants.DELETE_ENUM_MEMBER_ID:
		return DeleteEnumMemberEvent(event_data["id"], event_data["value"])

def integrate_to_ida(event_dict):
	pass

class integrator(idaapi.UI_Hooks, idaapi.plugin_t):
	flags = idaapi.PLUGIN_HIDE | idaapi.PLUGIN_FIX
	comment = " "
	help = " "
	wanted_name = "Integrator"
	wanted_hotkey = ""

	def run(self):
		pass

	def init(self):	
		self._window_handler = create_hidden_window()
		self._id = insert_to_registery(self._window_handler)
		log("Created window")
		shared.INTEGRATOR_WINDOW_ID = self._id
		if shared.COMMUNICATION_MANAGER_WINDOW_ID != -1: #TODO open the communication manager
			shared.start_communication_manager()
		return idaapi.PLUGIN_KEEP

	def term(self):
		#win32gui.DestroyWindow(self._window_handler)
		remove_key_from_reg(self._id)
		self._id = 0
		
def PLUGIN_ENTRY():
	return integrator()
