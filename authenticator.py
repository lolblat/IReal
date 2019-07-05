"""
    This plugin is handling the authentication to the server, and to select project to work on.
"""
import requests
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
from forms.ProjectSelector import ProjectSelector
from forms.Auth import AuthForm
import json

#TODO add open pdb file and choose project to work on.
def log(data):
	print("[Authenticator] " + data)

def request_project_list():
	array_result = []
	headers = {"Authorization" : "Bearer {0}".format(base64.b64encode(shared.USER_TOKEN))}
	try:
		result = requests.get("{0}/{1}".format(constants.BASE_URL, constants.REQUEST_PROJECT_LIST.format(str(shared.USERID))), headers = headers)
		project_headers = json.loads(result.content)
	except Exception as e:
		return []
	for project_header in project_headers:
		array_result.append("{0} : {1}".format(project_header["id"], project_header["name"]))
	return array_result

class LiveHookIDP(ida_idp.IDP_Hooks):	
	def	ev_newfile(self, fname):	
		log("START")
		selector = ProjectSelector(request_project_list())
		selector.Compile()
		selector.Execute()
		return ida_idp.IDP_Hooks.ev_newfile(self, fname)

	def ev_oldfile(self, fname):
		log("START")
		selector = ProjectSelector(request_project_list())
		selector.Compile()
		selector.Execute()
		return ida_idp.IDP_Hooks.ev_oldfile(self, fname)

class authenticator(idaapi.UI_Hooks, idaapi.plugin_t):
	flags = idaapi.PLUGIN_HIDE | idaapi.PLUGIN_FIX
	comment = " "
	help = " "
	wanted_name = "Authenticator"
	wanted_hotkey = ""

	def run(self):
		pass

	def init(self):
		auth = AuthForm()
		auth.Compile()
		auth.Execute()
	
		if shared.IS_COMMUNICATION_MANAGER_STARTED:
			communication_manager_window_handler = constants.get_window_handler_by_id(shared.COMMUNICATION_MANAGER_WINDOW_ID)
			constants.send_data_to_window(communication_manager_window_handler, constants.CHANGE_USER, json.dumps({"username":shared.USERNAME, "id": shared.USERID, "token": shared.USER_TOKEN}))
		
		if idc.GetIdbPath(): #You open IDA directly with a file.
			selector = ProjectSelector(request_project_list())
			selector.Compile()
			selector.Execute()
		shared.PROJECT_ID = -1
		if shared.IS_COMMUNICATION_MANAGER_STARTED:
			communication_manager_window_handler = constants.get_window_handler_by_id(shared.COMMUNICATION_MANAGER_WINDOW_ID)
			constants.send_data_to_window(communication_manager_window_handler, constants.CHANGE_PROJECT_ID, json.dumps({"project-id": shared.PROJECT_ID}))
		
		self._live_hook = LiveHookIDP()
		self._live_hook.hook()
		self.hook()
		return idaapi.PLUGIN_KEEP

	def term(self):
		self.unhook()
		
def PLUGIN_ENTRY():
	return authenticator()
