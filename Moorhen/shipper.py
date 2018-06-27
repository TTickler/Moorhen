import json
import os
import snmp_interface
import sys
import pprint
import c_parser
import elasticsearch
from datetime import datetime

#if used, change to 'import elasticsearch_connection' to be more pythonic
#from elasticsearch_connection import Query


class Shipper(object):
    def __init__(self, shipperType, configPath):
        self.shipperType = shipperType
        self.configPath = configPath

        self._toShipOIDdict = {}


	self.generalConfigParser = c_parser.generalConfigParser()
        self.hardwareParser = c_parser.shipperConfigParser('hardware')
        self.snmpInterface = snmp_interface.snmpInterface()
        #
        self.toShipOIDdict = self.hardwareParser.parsedDict

    def setConfigPath(self, path):
        self.configPath = path

    @property
    def getType(self):
        return self.shipperType

    @property
    def getConfigPath(self):
        return self.configPath

    @property
    def toShipOIDdict(self):
        return self._toShipOIDdict

    @toShipOIDdict.setter
    def toShipOIDdict(self, parsedDict):
	self._toShipOIDdict.clear()
        temp_nested_dict = self.hardwareParser.nestedOIDs
        temp_nonNested_dict = self.hardwareParser.nonNestedOIDs

        #nested dict maker
        for topic in temp_nested_dict:
            for metricName in temp_nested_dict[topic]:
                for key, value in temp_nested_dict[topic][metricName].items():
			if key == 'Path':
				continue
			else:

				result = int(self.snmpInterface.getSnmpResult(value))

				#conditional to check if a status is reporting as not found
				#Since only three thresholds are supported in Grafana, 1 is converted 
				#to 4 to report as a failure 
				if key == 'Status' and result == 1:
					temp_nested_dict[topic][metricName][key] = 4
				
				else:
                			temp_nested_dict[topic][metricName][key] = result
				
				#temp_nested_dict[topic][metricName][key] = 4
        #nonNested dict maker
        for key, value in temp_nonNested_dict.items():
            temp_nonNested_dict[key] = float(self.snmpInterface.getSnmpResult(value))

        self._toShipOIDdict = temp_nested_dict
        self._toShipOIDdict['nonNested'] = temp_nonNested_dict
	
	#adding timestamp for indexing/querying purposes 
	self._toShipOIDdict['@timestamp'] = datetime.utcnow()
	self._toShipOIDdict['client'] = self.generalConfigParser.hostName


#interface for shipping hardware metrics defined in config file
class HardwareMetricShipper(Shipper):
    def __init__(self):

        #initialization of hardware type shipper
        Shipper.__init__("hardware", os.getcwd() + '/Config/shipperConfig.json')




#interface for shipping software metrics defined in config file
class SoftwareMetricShipper(Shipper):
    def __init__(self):

        #initialization of hardware type shipper
        Shipper.__init__("software", os.getcwd() + '/Config/shipperConfig.json')


#esTest = elasticsearch.Elasticsearch('http://localhost:9200')
#test = Shipper("hardware", os.getcwd() + '/Config/shipperConfig.json')
#pprint.pprint(test.toShipOIDdict)

#response = esTest.index(index="test",doc_type="systemstatus", body=test.toShipOIDdict)





