import json
import elasticsearch
import os
from pathlib import Path
import time
import pprint
from datetime import datetime

class indexHealth(object):
	def __init__(self):

		#expectedMetrics.json houses metrics with a format of CPU.1.Status where
		#CPU is the category, 1 is which metric within that category, and status is the actual
		#status returned from an snmpget on the specific OID. This simple format allows a readable 
		#configuration file and provides an easy format for splitting the strings into seperate keys for
		#queries 
		with open(os.getcwd() + '/expectedMetrics.json') as expectedMetricsJson:
			self.expectedMetrics = json.load(expectedMetricsJson)
	
	#returns status (2,3,4) of previous #totalToQuery oidTypes   
	def getCurrent(self ,greenTotal,oidType, hits_Source):
		
		#totalCount is a dictionary that keeps track of the count of OID statuses that are
		# 2, 3, or 4. The fields are incremented each time a specific status is found. So if 
		# CPU.1.Status = 2 totalCount would be {"2":1,"3":0,"4":0} after one iteration. This allows ease of
		# importance comparisons (4 > 3, 3 > 2) 
		totalCount = {"2":0, "3":0, "4":0}
				
		#loop to check status numbers 
		for category in hits_Source:
			if category == "nonNested" or category == "@timestamp" or category == "client":
				continue
			else:
				#for hardware piece in passed in hits[_source]. This is all of the hits returned from an
				#elasticsearch query in json formatting
				for hwPiece in hits_Source[category]:	
					for metric in hits_Source[category][hwPiece]:

						#conditional for comparing the expectedMetrics to the current metric. If it is found
						#then logic can be done to perform updates on totalCount's fields. Format of the current
						#metric is converted to EX: CPU.1.Status to match schema of expectedMetrics and match
						#how elasticsearch queries require their query to be formatted 
						if str(category + "." + hwPiece + "." + metric) in self.expectedMetrics['expectedMetrics']:
							if hits_Source[category][hwPiece][metric] == 2 and self.expectedMetrics['expectedMetrics'][str(category + "." + hwPiece + "." + metric)] != hits_Source[category][hwPiece][metric]:
								totalCount["4"] += 1
							elif hits_Source[category][hwPiece][metric] == 2:
								totalCount["2"] += 1
							elif hits_Source[category][hwPiece][metric] == 3:
								totalCount["3"] += 1
							else:
								totalCount["4"] += 1

						else:
							continue


		if totalCount["4"] != 0:
			status = 4
		elif totalCount["4"] == 0 and totalCount["3"] != 0:
			status = 3
		else:
			status = 2
								
		return status

	def queryIndex(self, index, docType, elasticsearch, querySize):
		esQuery = {"query": {
        			"type" : {
            				"value" : docType
       					 }	
    				   },

				    "sort": {
				      "@timestamp": {
        					"order":"desc"
      						}
					},

				"size": querySize
			}
		result = elasticsearch.search(index=index,doc_type=docType, body=esQuery)

		return result
		

	
	def putIntoIndex(self, body, elasticsearch):
		response = elasticsearch.index(index="test",doc_type="indexstatus", body=body)
		


if __name__ == '__main__':
	while True:


		test = indexHealth()
		es = elasticsearch.Elasticsearch("http://localhost:9200")
		
		res = test.queryIndex("test","systemstatus",es,5)
		#for hit in res["hits"]["hits"]:
		#	pprint.pprint(hit["_source"])

		print(test.getCurrent(5,5, res["hits"]["hits"][0]["_source"]))
		test.putIntoIndex({"@timestamp": datetime.utcnow(),"groupBy": "3" ,"overallStatus": test.getCurrent(5,5, res["hits"]["hits"][0]["_source"])}, es)
		#es = elasticsearch.Elasticsearch()
    		
		time.sleep(10)
