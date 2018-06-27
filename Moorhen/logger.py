import logging 


'''Python provides a logging module, but the goal here is to 
	provide a more readable interface and provide a Logger 
	in the form of an object.'''
class Logger(object):
	def __init__(self):
		self._filename = ''
		self._date_format = ''

	def initialize(self, filename, date_format):
		self.filename = filename
		self.date_format = date_format

		return self

	@property
	def filename(self):
		return self._filename

	@filename.setter
	def filename(self, filename):
		self._filename = filename

	@property
	def date_format(self):
		return self._date_format

	@date_format.setter
	def date_format(self, date_format):
		self._date_format = date_format

	@property
	
