from IEvent import IEvent

class ExitIDBEvent(IEvent):
	def __init__(self):
		super(ExitIDBEvent, self).__init__(24, "Exit from IDA", {})