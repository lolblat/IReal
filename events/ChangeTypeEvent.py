import IEvent

class ChangeTypeEvent(IEvent):
	def __init__(self, linear_address, variable_type):
		self.IEvent.__init__(6, "Change type", {"linear-address": linear_address, "variable-type": variable_type})