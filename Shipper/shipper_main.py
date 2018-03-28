import json
import os
import snmp_interface
import sys
import time
import pprint
import elasticsearch
from datetime import datetime
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
    dir_monitor = monitor.DirectoryMonitor()
    proc_monitor = monitor.ProcessMonitor()
    metric_monitor = monitor.MetricMonitor()
    
    message_objects_dict = msg_parser.messages
 
    #grabs list of all valid messages in regards to set schema
    endpoints = []
    for message_type in message_objects_dict:
	for message_object in message_objects_dict[message_type]:
	    for endP in message_object.endpoints:
                if endP in endpoints:
	            continue
	        else:
	            endpoints.append(endP)

    
    print(config_parser.sections())
    endpoint_threads = []
    for section in config_parser.sections():
	#try:
	thread = endpoint.Endpoint(config_parser.get(section, "host"), config_parser.get(section, "port"), section)
	endpoint_threads.append(thread)
	thread.daemon = True
	thread.name = section
	thread.start()
	#except:
	 #   print("Invalid section configuration in endpoints.ini. Check format.")

    i = 0
    while True:
	for thread in endpoint_threads:
	    print(endpoint_threads)
	    thread.fifo_queue.enqueue("NICENICE " + str(i))
	    i += 1
	    print(thread.fifo_queue.dequeue())
	    time.sleep(5)






