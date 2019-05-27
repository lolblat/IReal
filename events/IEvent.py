import json

def decode_bytes(val):
	if not isinstance(val, str):
		return val
	return val.decode("raw_unicode_escape")

def encode_bytes(val):
	if not isinstance(val, str):
		return val
	return val.encode("raw_unicode_escape")
class IEvent(object):
	def __init__(self, event_id, name, data):
		self.id = event_id
		self.name = name
		self.data = data

	def encode_to_json(self):
		return json.dumps({"id": self.id,
				"name": self.name,
				"data": self.data})

	def implement(self):
		pass