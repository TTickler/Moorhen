import json
import os
import snmpInterface
import sys
import time
import pprint
from cParser import *
import elasticsearch
from datetime import datetime
from Shipper import *

class ShipperMain(object):
    def __init__(self):
        self.test = 5






if __name__ == '__main__':
	while True:
    		shipper = ShipperMain()
		esTest = elasticsearch.Elasticsearch('http://localhost:9200')
		test = Shipper("hardware", os.getcwd() + '/Config/shipperConfig.json')
		response = esTest.index(index="test",doc_type="systemstatus", body=test.toShipOIDdict)
		time.sleep(5)

