import socket
import struct
import pprint
#for future use to allow multiple endpoints to have
#data shipped to them asynchro
import threading
import Queue
import logging
import time 
import json



'''First in first out queue interface for endpoints to have for messages attempting to reach 
	specified endpoint. 

	Ex. Logstash-1 is an Endpoint that has been successfully instantiated and connected through
		a TCP socket. A message configured to be shipped to Logstash-1 will be placed in the 
		queue of the Logstash-1 Endpoint object.'''
class FIFOQueue(object):
	def __init__(self):
	
		self.items = []

		#setup logger here or in main interface for Shipper

	@property
	def queue_size(self):
		return len(self.items)

	
	def dequeue(self):
		
		#attempts to dequeue the first element
		#if it fails the queue is empty
		
			
		element = self.items.pop()
		#except:
		#	print("Queue is empty.")
		#	element = ''
		return element

	def enqueue(self, message):

		try:

			self.items.insert(0, message) 

		except:
			print("Failed to place " + str(message) + " into " + str(self.queue))

	#returns True if queue is empty and false if message is in queue
	def is_empty(self):
		
		if self.queue_size == 0:
			return True
		else:
			return False

	def print_queue(self):
	    
	    for element in self.items:
		pprint.pprint(element)



class Endpoint(threading.Thread):

	#As of now, no init parameters needed as
	#goal is to be property based Endpoint
	#name argument is for unique identifier of each object
	def __init__(self, address, port, name):
		threading.Thread.__init__(self)
		self._address = address
		self._port = port
		self.fifo_queue = FIFOQueue()

		self.init_socket()
		self.sock_connect()
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
                self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


	#attempts to close socket
	def close_connection(self):
		try:
			self._socket.close()
			print("Successfully closed socket: " + self.address + ":" + str(self.port))

		except:
			print("Failed to close socket: " + self.address + ":" + str(self.port))

	''''''
	def sock_connect(self):

		#originally was to be provided as configurable, but 
		#no reason to pollute configuration files. Easily changeable here
		max_conn_attempts = 5
		
		if self.address == '' or self.port == 0:
			return False

		else:
			try:
				self._socket.connect((self.address, int(self.port)))
    				l_onoff = 1                                                                                                                                                           
    				l_linger = 0                                                                                                                                                          
    				self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER,                                                                                                                     
                 			struct.pack('ii', l_onoff, l_linger))


			except socket.error as message:
				print(message)

				#Change from hardcoded value to configurable value
				#Prefer to have a default value of 3-5 connection attempts before
				#closing thread
				for attempt in range(0, max_conn_attempts):
					print("\n\nAttempting to connect again...")
					try:
						self._socket.connect((self.address, int(self.port)))
					except socket.error as msg:
						print msg
				return False


	'''Returns True if socket connection is reset and connected
		successfully. False if otherwise.'''
	def reset_connection(self):
		
		#try:
		self.close_connection()
		self.init_socket()
		self.sock_connect()
		#self._socket.connect((self.address, int(self.port)))
		#print("Successfully reset socket connection")
		#	return True
		#except:
		#	print("Failed to reset socket connection")
		#	return False
	
	def send(self, message):
		

		'''SEND THE MESSAGE OBJECT'S PAYLOAD. NOT THE MESSAGE ITSELF'''
	
		try:
			self._socket.sendall(message)

		except socket.error as msg:	
			print("Message failed to send over port " + str(self.port) + " to host " + self.address)
			print("Resetting connection...")
			self.reset_connection()



	''''''
	def run(self):
			
		while True:

			print("reeE")
			if self.fifo_queue.is_empty() is False:
				curr_message = self.fifo_queue.dequeue()


				message = curr_message
				to_send = {"message": message, "tags": ['test'], "fields": {"test": "test"}}
				print("to_send:  " + str(to_send))
				self.send(json.dumps(to_send))
			
		#	self.fifo_queue.print_queue()
			time.sleep(5)
