import json
import elasticsearch
import os
from pathlib import Path
import time
import pprint
from datetime import datetime
import ConfigParser


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
	def getCurrent(self ,greenTotal,oidType, hits_source, Config, elasticsearch):
		print(hits_source)
		#totalCount is a dictionary that keeps track of the count of OID statuses that are
		# 2, 3, or 4. The fields are incremented each time a specific status is found. So if 
		# CPU.1.Status = 2 totalCount would be {"2":1,"3":0,"4":0} after one iteration. This allows ease of
		# importance comparisons (4 > 3, 3 > 2) 
		totalCount = {"1": 0, "2":0, "3":0, "4":0}

		
		#loop to check status numbers 
		for category in hits_source:
			if category == "@timestamp" or category == "client":
				continue

		                #query for specific node's expectedMetrics template from elasticsearch database
                	esQuery = {
                	  "query": {
                	        "match": {"client": hits_source["client"]}
                	        },
                 	 "size": "1",
                 	 "sort": [
                        	   {
                        		"@timestamp": {
                        		"order": "desc"
                             		 }
                           	 }
                             ]
                       	 }
			

			#gets the expected metrics for speficied host by querying specified index/doctype for 
			#mappings
			#expectedMetrics = self.queryES(Config.get(), Config.get(), elasticsearch)


                        elif category == "nonNested":
				for metric in hits_source[category]:
					
					#query templates index for expectedMetrics of current hostname for 
					#expected metric values for comparison to snmpget results from the specified node
					expectedMetrics = self.queryES(Config.get('Indices','templateIndex'), Config.get('Indices','templateDocType'), esQuery, elasticsearch)
					if str(metric) in expectedMetrics['']['Threshold']:

						#since certain metrics such as CPU Utilization can have a lower value being worse than a higher value
						#we must allow an easily configurable way to handle this. getcompareType returns whether the flow of comparisons
						#increase or decrease. CPU Util might look something like 90>80>70 where anything above 90 is healthy, 89-71 is
						#a warning area and anything less than 70 is a critical state. getCompareType() will return 'increasing' for less than and 'decreasing' for greater than
						compareType = self.getCompareType(self.expectedMetrics['expectedMetrics']['Threshold'][str(metric)])
						
						totalCount = self.thresholdChecker(category, metric, hits_source, compareType, totalCount, self.expectedMetrics['expectedMetrics']['Threshold'][str(metric)])
						

					else:
						continue
					


			else:
				#for hardware piece in passed in hits[_source]. This is all of the hits returned from an
				#elasticsearch query in json formatting
				for hwPiece in hits_source[category]:	
					for metric in hits_source[category][hwPiece]:

						#conditional for comparing the expectedMetrics to the current metric. If it is found
						#then logic can be done to perform updates on totalCount's fields. Format of the current
						#metric is converted to EX: CPU.1.Status to match schema of expectedMetrics and match
						#how elasticsearch queries require their query to be formatted 
						if str(category + "." + hwPiece + "." + metric) in self.expectedMetrics['expectedMetrics']['Status']['healthy']:
							totalCount = self.statusMetricsChecker(category, hwPiece, metric, hits_source, totalCount)

						elif str(category + ".*." + metric) in self.expectedMetrics['expectedMetrics']['Status']['healthy']:
							totalCount = self.statusMetricsChecker(category, metric, hits_source, totalCount, hwPiece, wildcard=True)
						else:
							continue
				
		print(totalCount)

		if totalCount["4"] != 0:
			status = 4
		elif totalCount["4"] == 0 and totalCount["3"] != 0:
			status = 3
		else:
			status = 2
								
		return status


	#returns true if sequential threshold is met which is configured in hubConfig.json
	def sequentialThresholdMet(self, metric, elasticsearch):
		


		return True


		return False

	def statusMetricsChecker(self, category, metric, hits_source, totalCount, hwPiece, wildcard=False):
                            

		#allows configuration to have wildcard for count of individual metric for brevity
		#hwPieceHolder should probably be changed in name to be more relevant and readable  
		if wildcard == True:
			hwPieceHolder = '*'
		else:
			hwPieceHolder = hwPiece

            	print(str(category + "." + hwPiece + "." + metric)) 
		if hits_source[category][hwPiece][metric] == self.expectedMetrics['expectedMetrics']['Status']['healthy'][str(category + "." + hwPieceHolder + "." + metric)]:
			totalCount["2"] += 1
		elif hits_source[category][hwPiece][metric] == self.expectedMetrics['expectedMetrics']['Status']['warning'][str(category + "." + hwPieceHolder + "." + metric)]:
			totalCount["3"] += 1
		elif hits_source[category][hwPiece][metric] == self.expectedMetrics['expectedMetrics']['Status']['failure'][str(category + "." + hwPieceHolder + "." + metric)]:
                        totalCount["4"] += 1
                else:
                        totalCount["1"] += 1

		return totalCount

	def getCompareType(self, metricDict):

		if metricDict["healthy"] > metricDict["warning"] and metricDict["warning"] > metricDict["critical"]:
			return 'decreasing'
		else:
			return 'increasing'


	def thresholdChecker(self, category, metric ,hits_source, compareType, totalCount, metricDict):
		print(metricDict)
		print(hits_source[category][metric])	
		if compareType == 'decreasing':
			if hits_source[category][metric] > metricDict['healthy']:
				totalCount["2"] += 1
			elif (hits_source[category][metric] < metricDict['healthy']) and (hits_source[category][metric] > metricDict['critical']):
				totalCount["3"] += 1

			else:
				totalCount["4"] += 1 

		else:
                        if hits_source[category][metric] > metricDict['critical']:
                                totalCount["4"] += 1
                        elif (hits_source[category][metric] > metricDict['healthy']) and (hits_source[category][metric] < metricDict['critical']):
                                totalCount["3"] += 1

                        else:
                                totalCount["2"] += 1

		return totalCount

	def queryES(self, index, docType, esQuery, elasticsearch):
		result = elasticsearch.search(index=index,doc_type=docType, body=esQuery)

		return result
		

	
	def putIntoIndex(self, body, elasticsearch):
		response = elasticsearch.index(index="test",doc_type="indexstatus", body=body)
		


if __name__ == '__main__':
		
	#open hubConfig.ini for parsing configurable values out such as 
	#the consecutive threshold hit limits 
	Config = ConfigParser.ConfigParser()
	Config.read(os.getcwd() + "hubConfig.ini")		


        es = elasticsearch.Elasticsearch("http://localhost:9200")
	test = indexHealth(es)

	#query to be used for systemstatus 
        esQuery = {"query": {
                       "type" : {
                            "value" : Config.get("Indices", "aggDocType")
                                }
                            },

                        "sort": {
                        "@timestamp": {
                            "order":"desc"
                                      }
                                },

                        "size": Config.get("Indices", "aggQuerySize")
                 }

        while True:

		#passes esQuery into queryIndex to get results of specified query
		res = test.queryES(Config.get("Indices", "aggIndex"), Config.get("Indices", "aggDocType"), esQuery, es)
		#for hit in res["hits"]["hits"]:
		#	pprint.pprint(hit["_source"])
		
		print(test.getCurrent(5,5, res["hits"]["hits"][0]["_source"]), Config)
		test.putIntoIndex({"@timestamp": datetime.utcnow(),"groupBy": "3" ,"overallStatus": test.getCurrent(5,5, res["hits"]["hits"][0]["_source"])}, es)
		#es = elasticsearch.Elasticsearch()
    		
		time.sleep(10)
