from IEvent import IEvent
class ChangeStructNameEvent(IEvent):
	def __init__(self, id_of_struct, name):
		super(ChangeStructNameEvent, self).__init__(16, "Change struct name", {"id": id_of_struct, "value": name})
