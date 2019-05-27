from IEvent import IEvent
import idc
import ida_struct
class ChangeStructItemEvent(IEvent):
	def __init__(self, id_of_struct, offset, value):
		super(ChangeStructItemEvent, self).__init__(25, "Change struct item name", {"value":offset, "id": id_of_struct, "name": value})
		self._id = id_of_struct
		self._offset = offset
		self._value = value

	def implement(self):
		idc.set_member_name(self._id, self._offset, self._value)