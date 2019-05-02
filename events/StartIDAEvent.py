from IEvent import IEvent

class StartIDAEvent(IEvent):
	def __init__(self):
		super(StartIDAEvent, self).__init__(25, "Start IDA", {})