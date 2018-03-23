import socket

#for future use to allow multiple endpoints to have
#data shipped to them asynchro
import threading
import Queue
import logging
import time 




'''First in first out queue interface for endpoints to have for messages attempting to reach 
	specified endpoint. 

	Ex. Logstash-1 is an Endpoint that has been successfully instantiated and connected through
		a TCP socket. A message configured to be shipped to Logstash-1 will be placed in the 
		queue of the Logstash-1 Endpoint object.'''
class FIFOQueue(object):
	def __init__(self):
			
		#instantiates queue object. maxsize argument 
		#allows configuration of max queue size allowed.
		#Anything less than or equal to zero means the queue size is 
		#infinite. I chose -1 to make it clear as 0 would appear to be
		#saying the queue cannot have any elements in it
		self.queue = Queue.Queue(maxsize=-1)

		#setup logger here or in main interface for Shipper
	

	@property
	def queue_size(self):
		return self.queue.qsize()

	
	def dequeue(self):
		
		#attempts to dequeue the first element
		#if it fails the queue is empty
		try:
			self.queue.get()
		except:
			print("Queue is empty.")

	def enqueue(self):
		self.queue. 

	#returns True if queue is empty and false if message is in queue
	def is_empty(self):
		
		if self.queue_size == 0:
			return True
		else:
			return False



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
