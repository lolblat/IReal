from IEvent import IEvent
class ChangeFunctionNameEvent(IEvent):
	def __init__(self,name, linear_address):
		self.IEvent.__init__(1, "Change function name", {"value": name, "linear-address": linear_address})