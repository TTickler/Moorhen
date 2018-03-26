import json


class Message(object):
	def __init__(self, number):

		self._number = number
		self._endpoints = []
		self._timestamp = ''
		self._payload = {}
		self._tags = []
		self._monitor_type = ''

	'''Acts similar to __init__(), but provides a more readable point of 
		"entry" to this interface. This way it's abundantly clear that 
		you are initializing a new message.'''
	def initialize(self, timestamp='', endpoints=[], payload={}):
		self.timestamp = timestamp
		self.endpoints = endpoints
		self.payload = json.dumps(payload) 

	@property 
	def timestamp(self):
		return self._timestamp

	@timestamp.setter
	def timestamp(self, time):
		self._timestamp = time

	@property
	def endpoints(self):
		return self._endpoints

	@endpoints.setter
	def endpoints(self, endpoints):
		self._endpoints = endpoints

	@property
	def payload(self):
		return self._payload

	@payload.setter
	def payload(self, payload):
		self._payload = payload 

	@property
	def tags(self):
		return self._tags

	@tags.setter
	def tags(self, tags):
		self._tags = tags

	@property
	def monitor_type(self):
		return self._monitor_type 

	@monitor_type.setter
	def monitor_type(self, monitor_type):
		self._monitor_type = monitor_type

