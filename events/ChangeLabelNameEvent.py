from IEvent import IEvent
import ida_name
from constants import *
class ChangeLabelNameEvent(IEvent):
	def __init__(self, linear_address,label_name):
		super(ChangeLabelNameEvent, self).__init__(CHANGE_LABEL_NAME_ID,"Label name", {
											"linear-address":linear_address,
											 "value": label_name
											 }
											 )
		self._ea = linear_address
		self._name = label_name
	def implement(self):
		ida_name.set_name(self._ea, self._name, ida_name.SN_LOCAL)