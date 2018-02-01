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

        self._OIDdict = {}

        self.hardwareParser = shipperConfigParser('hardware')


        self.snmpInterface = snmpInterface.snmpInterface()
        self.setOIDdict()


    def setConfigPath(self, path):
        self.configPath = path

    @property
    def getType(self):
        return self.shipperType

    @property
    def getConfigPath(self):
        return self.configPath


    def setOIDdict(self):
        self.OIDdict = {}

        dskDict = {}



    @property
    def OIDdict(self):
        return self._OIDdict

    @OIDdict.setter
    def OIDdict(self, ):



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

test.getOIDdict
print('/n')
pprint.pprint(test.getOIDdict)
