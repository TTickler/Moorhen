import json
import os
import snmp_interface
import sys
import time
import pprint
import elasticsearch
import datetime
import shipper, message, c_parser, monitor, endpoint
import ConfigParser
import threading 


class ShipperMain(object):
    def __init__(self):
        self.test = 5

    def config_parser_init(self):
	config_parser = ConfigParser.ConfigParser()
	config_parser.read(os.getcwd() + "/Config/endpoints.ini")

	return config_parser



#Main of shipper "beat". 
if __name__ == '__main__':

    ship_main = ShipperMain()
    config_parser = ship_main.config_parser_init()

    msg_parser = c_parser.messagesParser()

    #moniter module interface instantiations for aggregation and monitor handling
    monitor_interface = monitor.Monitor()
    aggregator = monitor.Aggregator()
    
    message_objects_dict = msg_parser.messages
    #grabs list of all valid messages in regards to set schema
    endpoints = []
    for message_type in message_objects_dict:
	for message_object in message_objects_dict:
	   # print(message_object.focus)
	    for endP in message_object.endpoints:
                if endP in endpoints:
	            continue
	        else:
	            endpoints.append(endP)

    #list to hold thread objects 
    endpoint_threads = []
    for section in config_parser.sections():
	try:
	    print section
 	    thread = endpoint.Endpoint(config_parser.get(section, "host"), config_parser.get(section, "port"), section)
	    endpoint_threads.append(thread)
	    thread.daemon = True
	    thread.name = section
 	    thread.start()
	except:
	    print("Invalid section configuration in endpoints.ini. Check format.")

    i = 0

#AFTER MESSAGE IS SET UP CAST IT BACK TO CHILD CLASS OF MONITOREDMESSAGE
    while True:
        for message_type in message_objects_dict:
	    for message_object in message_objects_dict:
		#print(message_object.low_level_aggs)
		#print(message_object.high_level_aggs)
	        
		#casting message_object to child interface of monitoredMessage
		message_object.__class__ = message.MonitoredMessage
		message_object.monitored_payload  = monitor_interface.results(message_object)
		#message_object.meta_data = {"timestamp": str(datetime.datetime.now()), "host": "colby"}	
		aggregated_results = aggregator.results(message_object)
		aggregated_results.update(message_object.meta_data["agg"])
		message_object.monitored_payload.update(message_object.meta_data["non_agg"])

	        for endpoint in message_object.endpoints:
		    for thread in endpoint_threads:
		   #try:
		        if str(endpoint) == str(thread.name):
			    print("\n\nENDPOINT: " + thread.name)	   
	            	    thread.fifo_queue.enqueue(aggregated_results)
			    thread.fifo_queue.enqueue(msg_parser.flatten(message_object.monitored_payload))	    
			    thread.fifo_queue.print_queue()

		    #except:
		     #   print("Failed to enqueue handled results for: " + str(endpoint) + " with message: " + str(message_object._number))


	time.sleep(1)
	


