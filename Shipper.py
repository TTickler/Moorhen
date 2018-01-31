import json
import os
import snmpInterface
import sys


class Shipper(object):
    def __init__(self, shipperType, configPath):
        self.shipperType = shipperType
        self.configPath = configPath


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

        with open(self.configPath) as config:
            configDict = json.load(config)

        sys.stdout.write('Initializing.')
        for oidType in configDict['shipperTypes'][self.shipperType]['metrics']['OIDs']:

            for oid in configDict['shipperTypes'][self.shipperType]['metrics']['OIDs'][oidType]:
                sys.stdout.write('.')
                if oidType == "Disk":
                    self.OIDdict['Disk ' + oid['Name'] + ' Path'] = oid['Path']
                    self.OIDdict['Disk ' + oid['Name'] + ' Available'] = self.snmpInterface.getSnmpResult(oid['Available'])
                else:
                    self.OIDdict[oidType + ' ' + oid] = self.snmpInterface.getSnmpResult(configDict["shipperTypes"][self.shipperType]['metrics']["OIDs"][oidType][oid])


    @property
    def getOIDdict(self):
        return self.OIDdict



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
print("\n\n" + test.getOIDdict)