import idaapi
from all_events import *
import idc
from ida_idp import IDB_Hooks, IDP_Hooks
from ida_kernwin import UI_Hooks

PAUSE_HOOK = False
def log(data, *args):
	print("[IReal] " + data.format(args))

class ClosingHook(idaapi.UI_Hooks):
	def __init__(self):
		idaapi.UI_Hooks.__init__(self)
	def term(self):
		pass_to_manager(ExitIDBEvent())

class LiveHookIDP(ida_idp.IDP_Hooks):
	def ev_undefine(self, ea):
		pass_to_manager(UndefineDataEvent(ea))
		return ida_idp.IDP_Hooks.ev_undefine(self, ea)

class LiveHook(ida_idp.IDB_Hooks):
	def renamed(self, ea, new_name, is_local_name):		
		if not PAUSE_HOOK:
			log("Name changed: {0}  = {1} | {2}".format(hex(ea),new_name, is_local_name))
			flags_of_address = idc.GetFlags(ea)
			if isFunc(flags_of_address):
				pass_to_manager(ChangeFunctionNameEvent(ea, new_name))
			elif flags_of_address != 0:
				#need to find out if lablel or just global var 
				if is_local_name:
					pass
		return ida_idp.IDB_Hooks.renamed(self,ea,new_name,is_local_name)

	def changing_cmt(self, ea, repeatable_cmt, newcmt):
		if not PAUSE_HOOK:
			log("New comment: {0} {1}".format(hex(ea), newcmt))
			pass_to_manager(ChangeCommentEvent(ea, newcmt, repeatable_cmt))
		return ida_idp.IDB_Hooks.changing_cmt(self,ea,repeatable_cmt, newcmt)

	def func_added(self,pfn):
		if not PAUSE_HOOK:
			pass_to_manager(NewFunctionEvent(int(pfn.start_ea), int(pfn.end_ea)))
		return ida_idp.IDB_Hooks.func_added(self, pfn)

	def set_func_start(self, pfn, new_start):
		if not PAUSE_HOOK:
			log("New start: {0}".format(new_start))
			name = get_func_name(new_start).name
			pass_to_manager(ChangeFunctionStartEvent(name, new_start))
		return ida_idp.IDB_Hooks.set_func_start(self, pfn, int(new_start))

	def set_func_end(self, pfn, new_end):
		if not PAUSE_HOOK:
			log("New end: {0}".format(new_end))
			name = get_func_name(pfn.start_ea).name
			pass_to_manager(ChnageFunctionEndEveent(name, new_end))
		return ida_idp.IDB_Hooks.set_func_end(self, pfn, new_end)

	def struc_created(self, struc_id):
		return ida_idb.IDB_Hooks.struc_created(self, struc_id)

	def struc_member_created(self, sptr, mptr):
		return ida_idb.IDB_Hooks.struc_member_created(self, sptr, mptr)
		
	def renaming_struc_member(self, sptr, mptr, newname):
		if not PAUSE_HOOK:
			pass_to_manager(ChangeStructItemEvent(sptr.id, mptr.get_soff(), new_name))
		return ida_idp.IDB_Hooks.renaming_struc_member(self, sptr, mptr, newname)

	def struc_member_deleted(self, sptr, member_id, offset):
		if PAUSE_HOOK:
			pass_to_manager(DeleteStructVariableEvent(sptr.id, offset))
		return ida_idp.IDB_Hooks.struc_member_deleted(self, sptr, member_id, offset)

	def changing_range_cmt(self, kind, a, cmt, repeatable):
		if not PAUSE_HOOK:
			if kind == 1:
				function_address = a.start_ea
				pass_to_manager(ChangeCommentEvent(function_address, cmt, "Function"))
		return ida_idp.IDB_Hooks.changing_range_cmt(self, kind, a, cmt, repeatable)	

	def enum_created(self, id):
		return ida_idp.IDB_Hooks.enum_created(self, id)

	def enum_member_created(self, id, cid):
		return ida_idp.IDB_Hooks.enum_member_created(self, id, cid)

	def enum_deleted(self, id):
		return ida_idp.IDB_Hooks.enum_deleted(self, id)		

	def extra_cmt_changed(self, ea, line_idx, cmt):
		if not PAUSE_HOOK:
			pass
		return ida_idp.IDB_Hooks.extra_cmt_changed(self, ea, line_idx, cmt)

def pass_to_manager(ev):
	print("Pass to manager")

class hook_manager(idaapi.UI_Hooks, idaapi.plugin_t):
	flags = idaapi.PLUGIN_HIDE | PLUGIN_FIX
	comment = " "
	help = " "
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
		pass

	def register_actions(self):
		pass
		

	def init(self):
		msg("[IReal]: Init done\n")
		msg("[IReal]: Waiting for auto analysing\n")
		self.ready_to_run = self.run_init
		self.idb_hook = LiveHook()
		#self.ui_hook = ClosingHook()
		#self.idp_hook = LiveHookIDP()
		self.idb_hook.hook()
		#self.ui_hook.hook()
		#self.idp_hook.hook()
		self.hook()
		return idaapi.PLUGIN_KEEP

	def term(self):
		pass
		

def PLUGIN_ENTRY():
	return hook_manager()
