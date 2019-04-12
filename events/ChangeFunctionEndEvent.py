from IEvent import IEvent

class ChangeFunctionEndEvent(IEvent):
	def __init__(self,name, value):
		super(ChangeFunctionEndEvent, self).__init__(10, "Change function end", {"name": name, "value": value})