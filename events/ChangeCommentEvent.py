from IEvent import IEvent

class ChangeCommentEvent(IEvent):
	def __init__(self, linear_address, value, comment_type):
		super().__init__(4, "Comments", {"linear-address": linear_address, "value": value, "comment-type": comment_type})