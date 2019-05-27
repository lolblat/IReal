from IEvent import IEvent
import ida_funcs
class ChangeFunctionStartEvent(IEvent):
	def __init__(self, ea, value):
		super(ChangeFunctionStartEvent,self).__init__(9, "Change function start", {"linear-address": ea, "value": value})
		self._ea = ea
		self._value = value
		
	def implement(self):
		ida_funcs.set_func_start(self._ea, self._value)