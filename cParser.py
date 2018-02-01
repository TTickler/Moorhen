import json
import os 
import pprint

#interface for parsing configuration files from /Config
class cParser(object):
	def __init__(self, configPath):
		self._parserType = ''

		#uses configDict.setter to parse entire config file and store in _configDict as dictionary
		self.configDict = configPath
		#do not confuse with configDict being set with configPath through configDict.setter. 
		#this stores actual configPath.
		self._configPath = configPath


	#gets all fields within dictionary provided. 
	'''
		{
		   "example":[	
			{ 
		            "name": "bill",
			    "age" : 35
			}
		
			]
		}
		
	''' 

	#Only the field "example" will be parsed out as name and age reside in a nested list of dictionaries.
	#Their keys are not accessible
	def getFields(self, dl, keys_list):
                if isinstance(dl, dict):
                        keys_list += dl.keys()
                        map(lambda x: self.getFields(x, keys_list), dl.values())
                elif isinstance(self.configDict, list):
                        map(lambda x: self.getFields(x, keys_list), dl)
               

	@property
	def configDict(self):
		return self._configDict
	
	@configDict.setter
        def configDict(self, configPath):
                with open(configPath) as config:
                        self._configDict = json.load(config)

        @property
        def fields(self):
		keys_list = []
    		self.getFields(self.configDict, keys_list)
		return keys_list



#child class of cParser providing an interface for parsing /Config/generalConfig.json
class generalConfigParser(cParser):
	def __init__(self):
		cParser.__init__(self, os.getcwd() + "/Config/generalConfig.json")
		


#child class of cParser providing an interface for parsing /Config/shipperConfig.json
class shipperConfigParser(cParser):
	def __init__(self, shipperType):
		cParser.__init__(self, os.getcwd() + "/Config/shipperConfig.json")
		
		self._nonNestedOIDs = {}		
		self._nestedOIDs = {}

		self._shipperType = shipperType
		self.parsedDict = self.configDict
		self.nonNestedOIDs = self.configDict
		self.nestedOIDs = self.configDict
	

	@property
	def parsedDict(self):
		return self._parsedDict

	@parsedDict.setter
	def parsedDict(self, dictData):
		self._parsedDict = self.configDict['shipperTypes'][self._shipperType]

	@property
	def oidDict(self):
		return self._oidDict

	@oidDict.setter
	def oidDict(self, dictData):
		self._oidDict = self.configDict['shipperTypes'][self._shipperType]['metrics']['OIDs']

	@property
	def nonNestedOIDs(self):
		return self._nonNestedOIDs

	@nonNestedOIDs.setter
	def nonNestedOIDs(self, dictData):
		for key in self.configDict['shipperTypes'][self._shipperType]['metrics']['OIDs']:
			if key != 'nestedMetrics':
				self._nonNestedOIDs[key] = self.configDict['shipperTypes'][self._shipperType]['metrics']['OIDs'][key]

	#Handles parsing/returning nested metrics based off of shipperConfig.json schema under "OIDs" field
        @property
        def nestedOIDs(self):
                return self._nestedOIDs

        @nestedOIDs.setter
        def nestedOIDs(self, dictData):
                for key in self.configDict['shipperTypes'][self._shipperType]['metrics']['OIDs']:
                        if key == 'nestedMetrics':
                                self._nestedOIDs[key] = self.configDict['shipperTypes'][self._shipperType]['metrics']['OIDs'][key]


        @property
        def shipperTypes(self):
                shipperTypes = []

                for types in self.configDict['shipperTypes']:
                        shipperTypes.append(types)

                return shipperTypes
 
		


test = shipperConfigParser('hardware')
print(test.fields)
print('\n\n')
#pprint.pprint(test.configDict)
#pprint.pprint(test.parsedDict)
pprint.pprint(test.nonNestedOIDs)
