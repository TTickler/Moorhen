import json
import pysnmp
import os



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





        return OIDdict
