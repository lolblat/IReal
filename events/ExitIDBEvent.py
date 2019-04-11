from IEvent import IEvent

class ExitIDBEvent(IEvent):
	def __init__(self):
		self.IEvent.__init__(24, "Exit from IDA", {})