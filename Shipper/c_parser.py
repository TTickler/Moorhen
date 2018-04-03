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
	
	messages = []
	filenames = self.get_filenames()

        #counter for creating unique message objects. Acts as an id. 
        id_counter = 0
	for filename in filenames:
	    try:
	        with open(self._messages_path + filename) as curr_json:
	            found_json = json.load(curr_json)	

            except:
                print("\nError Parsing " + filename + ". Not valid JSON.")
		continue 

            for message_json in found_json["messages"]:
	        
		#checks if message is valid according to schema
		if self.is_valid_schema(message_json):
		    #self.iniialized_message() returns a fully initialized Message object with unique counter ID 
		    temp_message = self.initialized_message(id_counter, message_json)
		    messages.append(temp_message)
		    id_counter += 1
		else:
		    continue
        

        return messages


    def initialized_message(self, id_counter, message_json):
	
	#instantiates Message object
	initialized_msg_object = message.Message(id_counter)
	initialized_msg_object.endpoints = self.get_endpoints(message_json)
	initialized_msg_object.monitor_name = self.get_monitor_name(message_json)
	initialized_msg_object.high_level_aggs = self.get_high_level_aggs(message_json)
	initialized_msg_object.low_level_aggs = self.get_low_level_aggs(message_json)	


	return initialized_msg_object

    def get_high_level_aggs(self, message):
	return message["aggs"]["HighLevelAggs"]

    def get_low_level_aggs(self, message):
	return message["aggs"]["LowLevelAggs"]

    def get_endpoints(self, message):
	return message["endpoints"]

    def get_monitor_name(self, message):
	return message["monitor_name"]

    def get_focus(self, message):
	return message["focus"]

    #checks if passed in message is valid according to set JSON schema
    #returns True if it is valid and false otherwise
    def is_valid_schema(self, message_json):
	

	'''These are placeholders for currently allowed fields in each relevant
		message type. Root level fields can be stored in a simple list while 
		nested fields are currently stored in a dictionary as this allows mutability
		for future functionality additions without much change'''
	message_fields = ["monitor_name", "focus", "endpoints", "aggs"]


	print(message_json)
	if "monitor_name" in message_json:
	    validity = self.fields_exist(message_json, message_fields)

	    if validity == True:
                return True

	    else:
		return False

	else:
            return False

    def fields_exist(self, message_json, expected_msg_fields):
	
	#checks if all expected fields are found in root of JSON object
	#returns false if ANY expected_field is not found in JSON object
	for expected_field in expected_msg_fields:
	    if expected_field not in message_json:
	        return False
		
	    else:
	        continue 
	
	return True

    def parse_json(self, filename):


        return parsed_json


    #returns all filenames in messages directory
    def get_filenames(self):
    
        filenames = []
        for filename in os.listdir(self._messages_path):
            filenames.append(filename)

        return filenames


test = messagesParser()
#print(test.messages)
objArray = test.messages
print("\nObject Array: " + str(objArray))
for obj in objArray:
    print("\nObject: " + str(obj))
    print("Object ID/Message Number: " + str(obj._number))
    print("Monitor Name: " + obj.monitor_name)
    print("Endpoints: " + str(obj.endpoints))
    print("\n")



