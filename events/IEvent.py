import json

class IEvent(object):
	def __init__(self, event_id, name, data):
		self.id = event_id
		self.name = name
		self.data = data

	def encode_to_json(self):
		return json.dumps({"id": self.id,
				"name": self.name,
				"data": self.data})
