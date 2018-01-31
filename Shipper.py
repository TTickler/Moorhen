import json
import os
import snmpInterface
import sys
import pprint

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

        dskDict = {}

        with open(self.configPath) as config:
            configDict = json.load(config)

	#Provides client ability to determine progress
        sys.stdout.write('Initializing.')

	#outer loop for parsing shipperConfig.json
        for oidType in configDict['shipperTypes'][self.shipperType]['metrics']['OIDs']:

            for oid in configDict['shipperTypes'][self.shipperType]['metrics']['OIDs'][oidType]:
                sys.stdout.write('.')
                if oidType == "Disk":
                    dskDict['Disk ' + oid['Name']] = {}
                    dskDict['Disk ' + oid['Name']].update({"Path": oid['Path']})
                    dskDict['Disk ' + oid['Name']].update({"Available": self.snmpInterface.getSnmpResult(oid['Available'])})

                    self.OIDdict.update(dskDict)
                    dskDict.clear()
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
print('/n')
pprint.pprint(test.getOIDdict)
