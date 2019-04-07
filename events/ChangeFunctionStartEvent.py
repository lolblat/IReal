import IEvent

class ChangeFunctionStartEvent(IEvent):
	def __init__(self, name, value):
		self.IEvent.__init__(9, "Change function start", {"name": name, "value": value})