import IEvent

class CreateStructEvent(IEvent):
	def __init__(name_of_struct, id_of_struct):
		self.IEvent.__init__(11, "Create new struct", {"name": name_of_struct, "id": id_of_struct})