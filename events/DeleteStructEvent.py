from IEvent import IEvent

class DeleteStructEvent(IEvent):
	def __init__(self, id_of_struct):
		super(DeleteStructEvent, self).__init__(15, "Delete struct", {"id": id_of_struct})