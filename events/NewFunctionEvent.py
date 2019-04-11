from IEvent import IEvent

class NewFunctionEvent(IEvent):
	def __init__(self, linear_address_start, linear_address_end):
		self.__init__.IEvent(7, "New function", {"linear-address-start": linear_address_start, "linear-address-end": linear_address_end})