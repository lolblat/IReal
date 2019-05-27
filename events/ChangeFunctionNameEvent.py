from IEvent import IEvent
import idc
class ChangeFunctionNameEvent(IEvent):
	def __init__(self,name, linear_address):
		super(ChangeFunctionNameEvent, self).__init__(1, "Change function name", {"value": name, "linear-address": linear_address})
		self._value = name
		self._linear_address = linear_address

	def implement(self):
		idc.MakeName(self._linear_address, self._value)