from IEvent import IEvent
class CreateStructVariableEvent(IEvent):
	def __init__(self, id_of_struct, offset, variable_type, value):
		super(CreateStructVariableEvent,self).__init__(12, "Create struct variable", {"id": id_of_struct, "offset": offset, "variable-type": variable_type, "value": value})	