from IEvent import IEvent


class ChangeGlobalVariableNameEvent(IEvent):
	def __init__(self, linear_address, new_name, is_public):
		super(ChangeGlobalVariableNameEvent, self).__init__(2,"Change global variable name", {"linear_address": linear_address, "value": new_name, "label-type": ("public" if is_public else "local") })