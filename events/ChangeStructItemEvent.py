from IEvent import IEvent

class ChangeStructItemEvent(IEvent):
	def __init__(self, id_of_struct, offset, value):
		super().__init__(25, "Change struct item name", {"value":offset, "id": id_of_struct, "name": value})