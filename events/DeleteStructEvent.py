import IEvent

class DeleteStructEvent(IEvent):
	def __init__(self, id_of_struct):
		self.IEvent.__init__(15, "Delete struct", {"id": id_of_struct})