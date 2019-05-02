from IEvent import IEvent

class CreateEnumEvent(IEvent):
	def __init__(self, name, id_of_enum):
		super(CreateEnumEvent, self).__init__(17, "Create enum", {"name": name, "id" :id_of_enum})