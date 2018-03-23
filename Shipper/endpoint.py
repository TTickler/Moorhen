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
		try:
			print("Creating Socket...")
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			

		except socket.error as message:
			print(message) 

	#attempts to close socket
	def close(self, socket):
		try:
			socket.close()
			print("Successfully closed socket: " + self.address + ":" + self.port)

		except:
			print("Failed to close socket: " + self.address + ":" + self.port)

	''''''
	def sock_connect(self):
		
		if self.address == '' or self.port == 0:
			return False

		else:
			try:
				sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				sock.

			except socket.error as message:
				print(message)

				#Change from hardcoded value to configurable value
				#Prefer to have a default value of 3-5 connection attempts before
				#closing thread
				for attempt in range(0, max_conn_attempts)
					print("\n\nAttempting to connect again...")
					self.sock_connect(
				
				return False


	'''Returns True if socket connection is reset and connected
		successfully. False if otherwise.'''
	def reset_connection(self, socket):
		
		try:
			socket.connect(self.address, self.port)
			print("Successfully reset socket connection")
			return True
		except:
			print("Failed to reset socket connection")
			return False
	
	def send(self, message):
		
		try:

		except socket.error as msg:	
			print("Message failed to send over port " + self.port + " to host " + self.address )
