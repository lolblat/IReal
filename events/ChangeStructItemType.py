from IEvent import IEvent

class ChangeSturctItemTypeEvent(IEvent):
	def __init__(self, id_of_struct, offset, variable_type):
		self.IEvent.__init__(14, "Change struct item type", {"id": id_of_struct, "offset": offset, "variable-type": variable_type})