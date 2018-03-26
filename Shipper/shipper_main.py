import json
import os
import snmpInterface
import sys
import time
import pprint
import elasticsearch
from datetime import datetime
import shipper, endpoint, message, monitor

class ShipperMain(object):
    def __init__(self):
        self.test = 5







#Main of shipper "beat". 
if __name__ == '__main__':
	while True:
		
		#should be changed to being parsed from generalConfig.py for host/port
		es = elasticsearch.Elasticsearch('http://localhost:9200')
		
		ship = shipper.Shipper("hardware", os.getcwd() + '/Config/shipperConfig.json')
		pprint.pprint(ship.toShipOIDdict)
		response = es.index(index="test",doc_type="systemstatus", body=ship.toShipOIDdict)
		
		#Can be changed based on preferences on system load vs. performance. The only visualizations to keep track of 
		#are visualizations relying heavily on time series data and matching expected index times such as graphs
		time.sleep(5)

