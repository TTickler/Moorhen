import elasticsearch
from datetime import datetime


class Status(object):
	def __init__(self):
		self.test = 5


	@property
	def overallStatus(self):
		return self._overallStatus

	@overallStatus.setter
	def overallStatus(self, status):
		self._overallStatus = status


	#helper functions
	def setOverallStatus(self, metrics_dict):
		
		for typeMetric in metrics_dict:
			for 
		



class systemStatus(Status):
	def __init__(self):
		Status.__init__()




class siteStatus(Status):
	def __init__(self):
		Status.__init__()


