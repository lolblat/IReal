from IEvent import IEvent
import ida_struct
class ChangeStructNameEvent(IEvent):
	def __init__(self, id_of_struct, name):
		super(ChangeStructNameEvent, self).__init__(16, "Change struct name", {"id": id_of_struct, "value": name})
		self._id = id_of_struct
		self._name = name

	def implement(self):
		ida_struct.set_struc_name(self._id, self._name)