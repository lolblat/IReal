import IEvent

class ChangeLabelNameEvent(IEvent):
	class __init__(self, linear_address,label_name):
		self.IEvent.__init__(3,"Label name", {
											"linear-address":linear_address,
											 "value": label_name
											 }
											 )