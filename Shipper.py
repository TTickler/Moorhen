import json
import pysnmp
import os
import


class Shipper(object):
    def __init__(self, shipperType, configPath):
        self.shipperType = shipperType
        self.configPath = configPath


    def setConfigPath(self, path):
        self.configPath = path



    @property
    def getType(self):
        return self.shipperType

    @property
    def getConfigPath(self):
        return self.configPath

    @property
    def getOIDdict(self):
        OIDdict = {}

        with open(self.configPath) as config:
            configDict = json.loads(config)

        for oidType in configDict[self.shipperType]["OIDs"]:
            for oid in oidType:
                if oidType == "Disk":
                    OIDdict['Disk ' + oid['name'] + ' Path'] = oid['Path']
                    OIDdict['Disk ' + oid['name'] + ' Available'] = self.
                else



        return OIDdict




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