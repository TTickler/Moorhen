import json
import os 

#interface for parsing configuration files from /Config
class cParser(object):
	def __init__(self, parserType):
		self.test = 5







#child class of cParser providing an interface for parsing /Config/generalConfig.json
class generalConfigParser(cParser):
	def __init__(self):
		cParser.__init__("general")
		


#child class of cParser providing an interface for parsing /Config/shipperConfig.json
class shipperConfigParser(cParser):
	def __init__(self):
		cParser.__init__("shipper")


