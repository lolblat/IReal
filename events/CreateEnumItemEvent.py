import IEvent
class CreateEnumItemEvent(IEvent):
	def __init__(self, id_of_enum, name, value):
		self.IEvent.__init__(18, "Create enum item", {"id": id_of_enum, "name": name, "value": value})