from IEvent import IEvent

class ChangeTypeEvent(IEvent):
	def __init__(self, linear_address, variable_type):
		super().__init__(6, "Change type", {"linear-address": linear_address, "variable-type": variable_type})