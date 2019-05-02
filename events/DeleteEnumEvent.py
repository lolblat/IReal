from IEvent import IEvent

class DeleteEnumEvent(IEvent):
	def __init__(self, id_of_enum):
		super(DeleteEnumEvent, self).__init__(20, "Delete enum", {"id": id_of_enum})