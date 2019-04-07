import IEvent

class DeleteEnumEvent(IEvent):
	def __init__(self, id_of_enum):
		self.IEvent.__init__(20, "Delete enum", {"id": id_of_enum})