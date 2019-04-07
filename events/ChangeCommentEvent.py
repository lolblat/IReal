import IEvent

class ChangeCommentEvent(IEvent):
	def __init__(self, linear-address, value, comment_type):
		self.IEvent.__init__(4, "Comments", {"linear-address": linear-address, "value": value, "comment-type": comment_type})