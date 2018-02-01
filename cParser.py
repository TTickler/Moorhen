import json
import os 

#interface for parsing configuration files from /Config
class cParser(object):
	def __init__(self, parserType):
		self.parserType = parserType
		
		if parserType == 'general':
			config_path = os.getcwd() + '/Config/generalConfig.json'
		else:
                        config_path = os.getcwd() + '/Config/shipperConfig.json'
		self.setConfigDict(config_path)


	def setConfigDict(self, configPath):
		with open(configPath) as config:
			self.configDict = json.load(config)
		return self.configDict 

	@property
	def ConfigDict(self):
		return self.configDict

        @property
        def Fields(self):
		keys_list = []
    		if isinstance(self.configDict, dict):
        		keys_list += dl.keys()
        		map(lambda x: get_keys(x, keys_list), dl.values())
    		elif isinstance(dl, list):
       			map(lambda x: get_keys(x, keys_list), dl)
		return keys_list



#child class of cParser providing an interface for parsing /Config/generalConfig.json
class generalConfigParser(cParser):
	def __init__(self):
		cParser.__init__(self, "general")
		


#child class of cParser providing an interface for parsing /Config/shipperConfig.json
class shipperConfigParser(cParser):
	def __init__(self):
		cParser.__init__(self, "shipper")




test = shipperConfigParser()
print(test.Fields)


