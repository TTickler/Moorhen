import json
import os
import snmpInterface
import sys
import pprint
from cParser import *

class Shipper(object):
    def __init__(self, shipperType, configPath):
        self.shipperType = shipperType
        self.configPath = configPath

        self._toShipOIDdict = {}

        self.hardwareParser = shipperConfigParser('hardware')
        self.snmpInterface = snmpInterface.snmpInterface()
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
        temp_nested_dict = self.hardwareParser.nestedOIDs
        temp_nonNested_dict = self.hardwareParser.nonNestedOIDs

        #nested dict maker
        for topic in temp_nested_dict:
            for metricName in temp_nested_dict[topic]:
                for key, value in temp_nested_dict[topic][metricName].items():
                    temp_nested_dict[topic][metricName][key] = self.snmpInterface.getSnmpResult(value)

        #nonNested dict maker
        for key, value in temp_nonNested_dict.items():
            temp_nonNested_dict[key] = self.snmpInterface.getSnmpResult(value)

        self._toShipOIDdict = temp_nested_dict
        self._toShipOIDdict['nonNested'] = temp_nonNested_dict




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



test = Shipper("hardware", os.getcwd() + '/Config/shipperConfig.json')
pprint.pprint(test.toShipOIDdict)
