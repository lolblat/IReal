from IEvent import IEvent
import ida_enum
class DeleteEnumEvent(IEvent):
	def __init__(self, id_of_enum):
		super(DeleteEnumEvent, self).__init__(20, "Delete enum", {"id": id_of_enum})
		self._id = id_of_enum
	
	def implement(self):
		ida_enum.del_enum(self._id)