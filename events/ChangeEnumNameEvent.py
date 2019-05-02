from IEvent import IEvent

class ChangeEnumNameEvent(IEvent):
	def __init__(self, id_of_enum, value):
		super(ChangeEnumNameEvent, self).__init__(21, "Change enum name", {"id": id_of_enum, "value": value})