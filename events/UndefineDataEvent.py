from IEvent import IEvent
import ida_bytes
class UndefineDataEvent(IEvent):
	def __init__(self, linear_address):
		super(UndefineDataEvent, self).__init__(8, "Undefine data", {"linear-address": linear_address})
		self._ea = linear_address

	def implement(self):
		ida_bytes.del_items(self._ea)