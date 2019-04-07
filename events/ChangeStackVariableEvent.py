import IEvent

class ChangeStackVariableEvent(IEvent):
	def __init__(self, linear_address, offset, value):
		self.IEvent.__init__(5, "Change stack variable name", {"linear-address": linear_address, "offset": offset, "value" : value})