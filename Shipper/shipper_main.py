import json
import os
import snmp_interface
import sys
import time
import pprint
import elasticsearch
from datetime import datetime
import shipper, message, c_parser, monitor

class ShipperMain(object):
    def __init__(self):
        self.test = 5







#Main of shipper "beat". 
if __name__ == '__main__':

    msg_parser = c_parser.messagesParser()
    dir_monitor = monitor.DirectoryMonitor()
    proc_monitor = monitor.ProcessMonitor()
    metric_monitor = monitor.MetricMonitor()
    
    message_objects_dict = msg_parser.messages
 
    #grabs list of all valid messages in regards to set schema
    endpoints = []
    for message_type in message_objects_dict:
	for message_object in message_objects_dict[message_type]:
	    for endpoint in message_object.endpoints:
                if endpoint in endpoints:
	            continue
	        else:
	            endpoints.append(endpoint)


    print(endpoints)

    #while True:
#	print(messages)






