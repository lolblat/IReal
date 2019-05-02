from IEvent import IEvent
class IDACursorEvent(IEvent):
	def __init__(self, linear_address):
		super(IDACursorEvent, self).__init__("23", "IDA cursor change", {"linear-address": linear_address})