import socket

#for future use to allow multiple endpoints to have
#data shipped to them asynchro
import threading

class Endpoint(object):

	#As of now, no init parameters needed as
	#goal is to be property based Endpoint
	def __init__(self):

		self._address = ''
		self._port = 0

	@property 
	def address(self):
		return self._address

	@address.setter
	def address(self, address):
		self._address = address

	@property 
	def port(self):
		return self._port
	
	@port.setter
	def port(self, port):
		self._port = port

	def init_socket(self):
		try 

	def connect(self):
		
		if self.address == '' or self.port == 0:
			return False

		else:
			try:
				sock = socket.socket(

			except socket.error as message:
				print(message)
				
				return False


	#add way to reset connection
	#def resetfunction()

	def send(self, message):
		
		try:

		except socket.error as msg:	
