import IEvent

class DeleteStructVariableEvent(IEvent):
	def __init__(self, id_of_struct, offset):
		self.IEvent.__init__(13, "Delete struct variable", {"id": id_of_struct, "offset": offset})