import idaapi
from events import *
import idc
from ida.idp import IDB_Hooks, IDP_Hooks
from ida_kernwin import UI_Hooks

PAUSE_HOOK = False

class ClosingHook(idaapi.UI_Hooks):
	def __init__(self):
		idaapi.UI_Hooks.__init__(self)
	def term(self):
		pass

class LiveHookIDP(ida_idp.IDP_Hooks):
	def ev_undefine(self, ea):
		print "[Sync-hook]: Undefined value: {0}".format(ea)
		idb_diff["names"][str(ea)] = None
		return ida_idp.IDP_Hooks.ev_undefine(self, ea)

class LiveHook(ida_idp.IDB_Hooks):
	def renamed(self, ea, new_name, is_local_name):		
		if not PAUSE_HOOK:
			print "[Sync-hook]: Name changed: {0}  = {1} | {2}".format(hex(ea),new_name, is_local_name)
			flags_of_address = idc.GetFlags(ea)
			if isFunc(flags_of_address):
				if str(ea) in idb_diff["functions"]:
					idb_diff["functions"][str(ea)]["function_name"] = new_name
				else:
					idb_diff["functions"][str(ea)] = {"function_name" : new_name}
			elif flags_of_address != 0:
				if is_local_name:
					idb_diff["names"][str(ea)] = new_name
				else:
					idb_diff["names"][str(ea)] = new_name
		return ida_idp.IDB_Hooks.renamed(self,ea,new_name,is_local_name)

	def changing_cmt(self, ea, repeatable_cmt, newcmt):
		res = ida_idp.IDB_Hooks.changing_cmt(self,ea,repeatable_cmt, newcmt)
		if not PAUSE_HOOK:
			print "[Sync-hook]: New comment: {0} {1}".format(hex(ea), newcmt)
			if repeatable_cmt:

				idb_diff["comments_repetable"][str(ea)] = newcmt
			else:
				idb_diff["comments_regular"][str(ea)] = newcmt
		return res

	def func_added(self,pfn):
		return ida_idp.IDB_Hooks.func_added(self, pfn)

	def set_func_start(self, pfn, new_start):
		if not PAUSE_HOOK:
			print "[Sync-hook] New start: {0}".format(new_start)
			old_start = int(pfn.start_ea)
			end = int(pfn.end_ea)
			name = sark.Line(old_start).name
			new_start = str(new_start)
			if new_start not in idb_diff["functions"]:
				idb_diff["functions"][new_start] = {"function_name" : name, "old_start": old_start}
		return ida_idp.IDB_Hooks.set_func_start(self, pfn, int(new_start))

	def set_func_end(self, pfn, new_end):
		if not PAUSE_HOOK:
			print "[Sync-hook] New end: {0}".format(new_end)
			function_address = str(pfn.start_ea)
			if function_address in idb_diff["functions"]:
				idb_diff["functions"][function_address]["endEA"] = new_end
			else:
				idb_diff["functions"][function_address] = {"endEA": new_end}
		return ida_idp.IDB_Hooks.set_func_end(self, pfn, new_end)

	def struc_created(self, struc_id):
		return ida_idb.IDB_Hooks.struc_created(self, struc_id)

	def struc_member_created(self, sptr, mptr):
		return ida_idb.IDB_Hooks.struc_member_created(self, sptr, mptr)
		
	def renaming_struc_member(self, sptr, mptr, newname):
		if not PAUSE_HOOK:
			offset_at_stack = str(mptr.get_soff())
			frame_id = str(sptr.id)
			if frame_id in idb_diff["frame_vars"]:
				idb_diff["frame_vars"][frame_id][offset_at_stack] = newname
			else:
				idb_diff["frame_vars"][frame_id] = {offset_at_stack: newname}
		return ida_idp.IDB_Hooks.renaming_struc_member(self, sptr, mptr, newname)

	def struc_member_deleted(self, sptr, member_id, offset):
		frame_id = str(sptr.id)
		if frame_id in idb_diff["frame_vars"]:
			idb_diff["frame_vars"][frame_id][str(offset)] = None
		else:
			idb_diff["frame_vars"][frame_id] = {str(offset): None}
		return ida_idp.IDB_Hooks.struc_member_deleted(self, sptr, member_id, offset)

	def changing_range_cmt(self, kind, a, cmt, repeatable):
		if not PAUSE_HOOK:
			if kind == 1:
				function_address = str(a.start_ea)
				if function_address in idb_diff["functions"]:
					idb_diff["functions"][function_address]["function_comment"] = cmt
				else:
					idb_diff["functions"][function_address] = {"function_comment": cmt}
		return ida_idp.IDB_Hooks.changing_range_cmt(self, kind, a, cmt, repeatable)	

	def enum_created(self, id):
		return ida_idp.IDB_Hooks.enum_created(self, id)

	def enum_member_created(self, id, cid):
		return ida_idp.IDB_Hooks.enum_member_created(self, id, cid)

	def enum_deleted(self, id):
		return ida_idp.IDB_Hooks.enum_deleted(self, id)		

	def extra_cmt_changed(self, ea, line_idx, cmt):
		if not PAUSE_HOOK:
			print "[Sync-hook] Extra cmt changed: {0} {1} {2}".format(ea,line_idx, cmt)
			if not cmt:
				idb_diff["comments_anterior"][str(ea)] = None
			else:
				if str(ea) in idb_diff["comments_anterior"]:
					idb_diff["comments_anterior"][str(ea)] += '\n' + cmt
				else:
					idb_diff["comments_anterior"][str(ea)] = cmt
		return ida_idp.IDB_Hooks.extra_cmt_changed(self, ea, line_idx, cmt)

def pass_to_manager(IEvent event):
	pass

class hook_manager(idaapi.UI_Hooks, idaapi.plugin_t):
	flags = idaapi.PLUGIN_HIDE | PLUGIN_FIX
	comment = "Push the xref, notes and functions names and addresses"
	help = "Push the xref, notes and functions names and addresses"
	wanted_name = "Hooker"
	wanted_hotkey = ""
	def run(self, arg):
		pass

	def run_init(self):
		global PAUSE_HOOK
		self.register_actions()
		self.attach_to_menu()
		PAUSE_HOOK = True
		auto_wait()
		PAUSE_HOOK = False

	def attach_to_menu(self):
		#idaapi.attach_action_to_menu("Edit/Plugins/Sync/Push database","sync:push_db", idaapi.SETMENU_APP)

	def register_actions(self):
		#idaapi.register_action(action_push_database)
		

	def init(self):
		msg("[SyncIDA]: Init done\n")
		msg("[SyncIDA]: Waiting for auto analysing\n")
		self.ready_to_run = self.run_init
		self.idb_hook = LiveHook()
		self.ui_hook = ClosingHook()
		self.idp_hook = LiveHookIDP()
		self.idb_hook.hook()
		self.ui_hook.hook()
		self.idp_hook.hook()
		self.hook()
		return idaapi.PLUGIN_KEEP

	def term(self):
		pass
		

def PLUGIN_ENTRY():
	return hook_manager()
