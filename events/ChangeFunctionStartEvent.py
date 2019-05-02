from IEvent import IEvent

class ChangeFunctionStartEvent(IEvent):
	def __init__(self, name, value):
		super(ChangeFunctionStartEvent,self).__init__(9, "Change function start", {"name": name, "value": value})