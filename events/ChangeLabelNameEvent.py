from IEvent import IEvent

class ChangeLabelNameEvent(IEvent):
	def __init__(self, linear_address,label_name):
		super().__init__(3,"Label name", {
											"linear-address":linear_address,
											 "value": label_name
											 }
											 )