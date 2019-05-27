from IEvent import IEvent
import ida_struct
class DeleteStructVariableEvent(IEvent):
	def __init__(self, id_of_struct, offset):
		super(DeleteStructVariableEvent, self).__init__(13, "Delete struct variable", {"id": id_of_struct, "offset": offset})
		self._id = id_of_struct
		self._offset = offset
		
	def implement(self):
		ida_struct.del_struc_member(self._id, self._offset)