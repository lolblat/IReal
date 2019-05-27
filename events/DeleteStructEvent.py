from IEvent import IEvent
import ida_struct
class DeleteStructEvent(IEvent):
	def __init__(self, id_of_struct):
		super(DeleteStructEvent, self).__init__(15, "Delete struct", {"id": id_of_struct})
		self._id = id_of_struct
	def implement(self):
		ida_stuct.del_struc(self._id)