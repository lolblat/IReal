from IEvent import IEvent

class UndefineDataEvent(IEvent):
	def __init__(self, linear_address):
		self.IEvent.__init__(8, "Undefine data", {"linear-address": linear_address})