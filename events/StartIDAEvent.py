from IEvent import IEvent

class StartIDAEvent(IEvent):
	def __init__(self):
		self.IEvent.__init__(25, "Start IDA", {})