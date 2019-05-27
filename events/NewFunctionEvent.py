from IEvent import IEvent
import ida_funcs
class NewFunctionEvent(IEvent):
	def __init__(self, linear_address_start, linear_address_end):
		super(NewFunctionEvent, self).__init__(7, "New function", {"linear-address-start": linear_address_start, "linear-address-end": linear_address_end})
		self._start = linear_address_start
		self._end = linear_address_end

	def implement(self):
		ida_funcs.add_func(self._start, self._end)