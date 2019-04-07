import IEvent

class ChangeFunctionHeaderEvent(IEvent):
	def __init__(self, linear_address, value):
		self.IEvent.__init__(22, "Change function header", {"linear-address": linear_address, 'value': value})