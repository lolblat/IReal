from IEvent import IEvent
import ida_funcs
class ChangeFunctionEndEvent(IEvent):
	def __init__(self, ea, value):
		super(ChangeFunctionEndEvent, self).__init__(10, "Change function end", {"linear-address": ea, "value": value})
		self._ea = ea
		self._new_end = value
	
	def implement(self):
		ida_funcs.set_func_end(self._ea, self._new_end)