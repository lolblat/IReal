from IEvent import IEvent, decode_bytes, encode_bytes
import ida_typeinf
from constants import *
class ChangeTypeEvent(IEvent):
	def __init__(self, linear_address, variable_type):
		super(ChangeTypeEvent, self).__init__(CHANGE_TYPE_ID, "Change type", {"linear-address": linear_address, "variable-type": [decode_bytes(t) for t in variable_type]})
		self._ea = linear_address
		self._type = [decode_bytes(t) for t in variable_type]
	def implement(self):
		py_type = [encode_bytes(t) for t in self._type]
		if len(py_type) == 3:
			py_type = py_type[1:]
		if len(py_type) >= 2:
			ida_typeinf.apply_type(
				None,
				py_type[0],
				py_type[1],
				self._ea,
				ida_typeinf.TINFO_DEFINITE,
			)
