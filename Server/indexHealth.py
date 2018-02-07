import json
import elasticsearch
import os


class indexHealth(object):
	def __init__(self):

		#expectedMetrics.json houses metrics with a format of CPU.1.Status where
		#CPU is the category, 1 is which metric within that category, and status is the actual
		#status returned from an snmpget on the specific OID. This simple format allows a readable 
		#configuration file and provides an easy format for splitting the strings into seperate keys for
		#queries 
		with open(os.getcwd() + '/expectedMetrics.json') as self.
	
	#returns status (2,3,4) of previous #totalToQuery oidTypes   
	def getCurrent(self,totalToQuery,greenTotal,oidType, hits):

		totalCount = {"2":0, "3":0, "4":0}
				
		#loop to check status numbers 
		for hit in hits:
			for key in hit:
				if key == 

		return status
		

	
	def putIntoIndex(self, body):
		response = self.es.index(index="indexhealth",doc_type="indexstatus", body=body)
		


if __name__ == '__main__':
	while True:
    		response = esTest.index(index="test",doc_type="systemstatus", body=test.toShipOIDdict)
		time.sleep(5)
 
