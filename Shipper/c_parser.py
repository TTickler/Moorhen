import json
import os
import pprint
import message


# interface for parsing configuration files from /Config
class cParser(object):
    def __init__(self, configPath):
        self._parserType = ''

        # uses configDict.setter to parse entire config file and store in _configDict as dictionary
        self.configDict = configPath
        # do not confuse with configDict being set with configPath through configDict.setter.
        # this stores actual configPath.
        self._configPath = configPath

    # gets all fields within dictionary provided.
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

    # Only the field "example" will be parsed out as name and age reside in a nested list of dictionaries.
    # Their keys are not accessible
    def getFields(self, dl, keys_list):
        if isinstance(dl, dict):
            keys_list += dl.keys()
            map(lambda x: self.getFields(x, keys_list), dl.values())
        elif isinstance(self.configDict, list):
            map(lambda x: self.getFields(x, keys_list), dl)

    #returns entirety of configuration as a dictionary 
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


# child class of cParser providing an interface for parsing /Config/generalConfig.json
class generalConfigParser(cParser):
    def __init__(self):
        cParser.__init__(self, os.getcwd() + "/Config/generalConfig.json")
	self._hostName = self.configDict['clientInfo']['name']

	#sets point of contact information parsed from generalConfig.json
	#PoC will be a dictionary with 'name' and 'phone' fields
	self._PoC = self.configDict['clientInfo']['Point of Contact']
    
    #returns hostName parsed from configuration file in __init__	
    @property
    def hostName(self):
    	return self._hostName

    @hostName.setter
    def hostName(self, name):
    	self._hostName = name


    #returns the point of contact dictionary parsed from generalConfig configuration file
    @property
    def pointOfContact(self):
	return self._pointOfContact

    @pointOfContact.setter
    def pointOfContact(self, PoC):
	self._pointOfContact = PoC

'''Child class of cParser. Crawls, and parses, all valid messages from all files '''
class messagesParser(cParser):
    def __init__(self):
	self._messages_path = os.getcwd() + "/Config/messages/"


    #updates messages dict accordingly based on valid messages with message objects
    @property
    def messages(self):
	
	messages = {"process":[], "directory":[], "metrics":[]}
	filenames = self.get_filenames()
	for filename in filenames:
	    	try:
		    with open(self._messages_path + filename) as curr_json:
		        found_json = json.loads(curr_json)	

		except:
            	    print("\nError Parsing " + filename + ". Not valid JSON.")
		    continue 

	    for message in found_json["messages"]:
	        
		#checks if message is valid according to schema
		if is_valid_schema(message):
		   self.initialize_message(message) 
		else:
		    continue
        

        return messages

    #checks if passed in message is valid according to set JSON schema
    #returns True if it is valid and false otherwise
    def is_valid_schema(self, message):

        return True

        return False

    def parse_json(self, filename):


    #returns all filenames in messages directory
    def get_filenames(self):
    
    filenames = []
    for filename in os.listdir(self._messages_path):
        filenames.append(filename)

    return filenames



