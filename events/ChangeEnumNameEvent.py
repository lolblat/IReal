import IEvent

class ChangeEnumNameEvent(IEvent):
	def __init__(self, id_of_enum, value):
		self.IEvent.__init__(21, "Change enum name", {"id": id_of_enum, "value": value, "name": name})