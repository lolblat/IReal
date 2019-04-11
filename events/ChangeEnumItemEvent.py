from IEvent import IEvent

class ChangeEnumItemEvent(IEvent):
	def __init__(self, id_of_enum, name, value):
		super().__init__(19, "Change enum item", {"id": id_of_enum, "name": name, "value": value})