import idaapi
import ida_enum
from all_events import *
import idc
import ida_bytes
from ida_idp import IDB_Hooks, IDP_Hooks
from ida_kernwin import UI_Hooks, View_Hooks
import ida_hexrays
import ida_typeinf
import ida_nalt
PAUSE_HOOK = True
last_ea = None
def log(data):
	print("[IReal] " + data)

class CursorChangeHook(ida_kernwin.View_Hooks):
	def view_loc_changed(self, view, now, was):
		if now.plce.toea() != was.plce.toea():
			pass_to_manager(IDACursorEvent(now.plce.toea()))

class ClosingHook(idaapi.UI_Hooks):
	def __init__(self):
		idaapi.UI_Hooks.__init__(self)

	def term(self):
		global PAUSE_HOOK
		PAUSE_HOOK = True
		log("Exit IDB")
		pass_to_manager(ExitIDBEvent())
		return idaapi.UI_Hooks.term(self)

	def postprocess_action(self):
		global last_ea
		address = idc.here()
		if address != 0xffffffff and address != 0xffffffffffffffff:
			if last_ea:
				if last_ea != address:
					pass_to_manager(IDACursorEvent(address))
					last_ea = address
			else:
				last_ea = address
				pass_to_manager(IDACursorEvent(address))

class LiveHookIDP(ida_idp.IDP_Hooks):
	def ev_undefine(self, ea):
		if not PAUSE_HOOK:
			pass_to_manager(UndefineDataEvent(ea))
		return ida_idp.IDP_Hooks.ev_undefine(self, ea)

	def	ev_newfile(self, fname):
		global PAUSE_HOOK
		log("START")
		pass_to_manager(StartIDAEvent())
		PAUSE_HOOK = False
		return ida_idp.IDP_Hooks.ev_newfile(self, fname)

	def ev_oldfile(self, fname):
		global PAUSE_HOOK
		log("START")
		pass_to_manager(StartIDAEvent())
		PAUSE_HOOK = False
		return ida_idp.IDP_Hooks.ev_oldfile(self, fname)

class LiveHook(ida_idp.IDB_Hooks):
	def closebase(self):
		global PAUSE_HOOK
		log("Exit IDB")
		pass_to_manager(ExitIDBEvent())
		PAUSE_HOOK = True
	def renamed(self, ea, new_name, is_local_name):		
		if not PAUSE_HOOK:
			log("Name changed: {0}  = {1} | {2}".format(hex(ea),new_name, is_local_name))
			flags_of_address = idc.GetFlags(ea)
			if isFunc(flags_of_address):
				pass_to_manager(ChangeFunctionNameEvent(ea, new_name))
			elif flags_of_address != 0:
				if is_local_name:
					pass_to_manager(ChangeLabelNameEvent(ea, new_name))
				else:
					pass_to_manager(ChangeGlobalVariableNameEvent(ea, new_name, not is_local_name))
		return ida_idp.IDB_Hooks.renamed(self,ea,new_name,is_local_name)

	def changing_cmt(self, ea, repeatable_cmt, newcmt):
		if not PAUSE_HOOK:
			log("New comment: {0} {1}".format(hex(ea), newcmt))
			pass_to_manager(ChangeCommentEvent(ea, newcmt, repeatable_cmt))
		return ida_idp.IDB_Hooks.changing_cmt(self,ea,repeatable_cmt, newcmt)

	def func_added(self,pfn):
		if not PAUSE_HOOK:
			log("New function")
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
			pass_to_manager(ChangeFunctionEndEveent(name, new_end))
		return ida_idp.IDB_Hooks.set_func_end(self, pfn, new_end)

	def struc_created(self, struc_id):
		if not PAUSE_HOOK:
			log("New struct")
			pass_to_manager(CreateStructEvent(ida_struct.get_struc_name(struc_id), struc_id))
		return ida_idp.IDB_Hooks.struc_created(self, struc_id)

	def renaming_struc(self, sid, oldname, newname):
		if not PAUSE_HOOK:
			log("Rename struct")
			pass_to_manager(ChangeStructNameEvent(sid, newname))
		return ida_idp.IDB_Hooks.renaming_struc(self, sid, oldname, newname)
	
	def struc_member_created(self, sptr, mptr):
		if not PAUSE_HOOK:
			tinfo = ida_typeinf.tinfo_t()
			ida_hexrays.get_member_type(mptr, tinfo)
			member_type = "unkown"
			if tinfo.get_size() == 1:
				member_type = 'db'
			elif tinfo.get_size() == 2:
				memeber_type = 'dw'
			elif tinfo.get_size() == 4:
				member_type = 'dd'
			elif tinfo.get_size() == 8:
				member_type = 'dq'
			else: #TODO: think what to do with custom struct vars like arrays or other structs.
				pass
			pass_to_manager(CreateStructVariableEvent(sptr.id, mptr.get_soff(), member_type, ida_struct.get_member_name(mptr.id)))
		return ida_idp.IDB_Hooks.struc_member_created(self, sptr, mptr)
		
	def renaming_struc_member(self, sptr, mptr, newname):
		if not PAUSE_HOOK:
			log("Rename struct member")
			pass_to_manager(ChangeStructItemEvent(sptr.id, mptr.get_soff(), newname))
		return ida_idp.IDB_Hooks.renaming_struc_member(self, sptr, mptr, newname)

	def struc_member_deleted(self, sptr, member_id, offset):
		if not PAUSE_HOOK:
			log("Remove struct memeber")
			pass_to_manager(DeleteStructVariableEvent(sptr.id, offset))
		return ida_idp.IDB_Hooks.struc_member_deleted(self, sptr, member_id, offset)
	def struc_deleted(self, struc_id):
		if not PAUSE_HOOK:
			log("Remove struct")
			pass_to_manager(DeleteStructEvent(struc_id))
		return 0
	def changing_struc_member(self, sptr, mptr, flag, ti, nbytes):
		if not PAUSE_HOOK:
			log("Changing struc member: {0} {1} {2} {3} {4}".format(sptr, mptr, flag, ti, nbytes))
			data_type = None
			if flag & ida_bytes.FF_BYTE:
				data_type = "db"
			elif flag & ida_bytes.FF_WORD:
				data_type = "dw"
			elif flag & ida_bytes.FF_DWORD:
				data_type = "dd"
			elif flag & ida_bytes.FF_QWORD:
				data_type = "dq"
			elif flag & ida_bytes.FF_STRUCT:
				data_type = ti.tid
			if data_type:
				pass_to_manager(ChangeStructItemEvent(sptr.id, mptr.get_soff(), data_type))
		return 0

	def changing_range_cmt(self, kind, a, cmt, repeatable):
		if not PAUSE_HOOK:
			if kind == 1:
				log("Change range comment {0} {1} {2} {3}".format(kind, ea, cmt, repeatable))
				function_address = a.start_ea
				pass_to_manager(ChangeCommentEvent(function_address, cmt, "Function"))
		return ida_idp.IDB_Hooks.changing_range_cmt(self, kind, a, cmt, repeatable)	

	def enum_created(self, id):
		if not PAUSE_HOOK:
			log("Enum created: {0}".format(id))
			pass_to_manager(CreateEnumEvent(ida_enum.get_enum_name(id), id))
		return ida_idp.IDB_Hooks.enum_created(self, id)

	def renaming_enum(self, eid, is_enum, newname):
		if not PAUSE_HOOK:
			log("Enum name changed")
			pass_to_manager(ChangeEnumNameEvent(eid, newname))
		return ida_idp.IDB_Hooks.renaming_enum(self, eid, is_enum, newname)

	def enum_member_created(self, id, cid):
		if not PAUSE_HOOK:
			log("Enum memeber created: {0} {1}".format(id, cid))
			enum_item_name = ida_enum.get_enum_member_name(cid)
			value = ida_enum.get_enum_member_value(cid)
			#TODO find how to get value from enum
			pass_to_manager(CreateEnumItemEvent(id, enum_item_name , value))
		return ida_idp.IDB_Hooks.enum_member_created(self, id, cid)

	def changing_enum_bf(self, id, value):
		if not PAUSE_HOOK:
			log("Enum member changed {0}".format(value))
			pass_to_manager(ChangeEnumItemEvent(ida_enum.get_enum_member_enum(id), ida_enum.get_enum_member_name(id), value))
		return ida_idp.IDB_Hooks.changing_enum_bf(self, id, value)

	def enum_deleted(self, id):
		if not PAUSE_HOOK:
			log("Enum deleted")
			pass_to_manager(DeleteEnumEvent(id))
		return ida_idp.IDB_Hooks.enum_deleted(self, id)		

	def extra_cmt_changed(self, ea, line_idx, cmt):
		if not PAUSE_HOOK:
			log("{0} {1}".format(line_idx, cmt))
			if line_idx / 1000 == 1:
				pass_to_manager(ChangeCommentEvent(ea, "{0}:{1}".format(line_idx, cmt), "anterior"))
			else:
				pass_to_manager(ChangeCommentEvent(ea, "{0}:{1}".format(line_idx, cmt), "posterior"))
		return ida_idp.IDB_Hooks.extra_cmt_changed(self, ea, line_idx, cmt)

	def ti_changed(self, ea, type, fnames):
		if not PAUSE_HOOK:
			log("Ti changed: {0} {1} {2}".format(str(ea), str(type), str(fnames)))
			flags_of_address = idc.GetFlags(ea)
			if isFunc(flags_of_address):
				tinfo = tinfo_t()
				ida_nalt.get_tinfo(ea, tinfo)
				pass_to_manager(ChangeFunctionHeaderEvent(ea, str(tinfo)))
			else:
				if flags_of_address & ida_bytes.FF_STRUCT:
					log(str(dir(type)))
				pass
		return ida_idp.IDB_Hooks.ti_changed(self, ea, type, fnames)

	def make_data(self, ea, flags, tid, len):
		#TODO figure out flags FF_*
		if not PAUSE_HOOK:
			log("Make data: {0} {1} {2} {3}".format(ea, flags, tid, len))
			data_type = None
			if flags & ida_bytes.FF_BYTE:
				data_type = "db"
			elif flags & ida_bytes.FF_WORD:
				data_type = "dw"
			elif flags & ida_bytes.FF_DWORD:
				data_type = "dd"
			elif flags & ida_bytes.FF_QWORD:
				data_type = "dq"
			elif flags & ida_bytes.FF_STRUCT:
				data_type = tid
			if data_type:
				pass_to_manager(ChangeTypeEvent(ea, data_type))
		return ida_idp.IDB_Hooks.make_data(self, ea, flags, tid, len)
		
	def auto_empty_finally(self):
		global PAUSE_HOOK
		log("auto finished")
		PAUSE_HOOK = False
		return 0
def pass_to_manager(ev):
	log("Pass to manager: " + str(ev))

class hook_manager(idaapi.UI_Hooks, idaapi.plugin_t):
	flags = idaapi.PLUGIN_HIDE | idaapi.PLUGIN_FIX
	comment = " "
	help = " "
	wanted_name = "Hooker"
	wanted_hotkey = ""
	def run(self, arg):
		pass

	def attach_to_menu(self):
		pass

	def register_actions(self):
		pass
		
	def init(self):
		global PAUSE_HOOK
		msg("[IReal]: Init done\n")
		msg("[IReal]: Waiting for auto analysing\n")
		PAUSE_HOOK = True
		self.idb_hook = LiveHook()
		self.ui_hook = ClosingHook()
		self.idp_hook = LiveHookIDP()
		self.view_hook = CursorChangeHook()
		self.idb_hook.hook()
		self.ui_hook.hook()
		self.idp_hook.hook()
		self.view_hook.hook()
		self.hook()
		return idaapi.PLUGIN_KEEP

	def term(self):
		pass
		#if self.idb_hook:
		#	self.idb_hook.unhook()
		#if self.ui_hook:
		#	self.ui_hook.unhook()
		#if self.idb_hook:
		#	self.idp_hook.unhook()
		
		

def PLUGIN_ENTRY():
	return hook_manager()
