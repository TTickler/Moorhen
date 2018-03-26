import json
import os
import snmp_interface
import sys
import time
import pprint
import elasticsearch
from datetime import datetime
import shipper, message, c_parser
#import endpoint, monitor

class ShipperMain(object):
    def __init__(self):
        self.test = 5







#Main of shipper "beat". 
if __name__ == '__main__':

    msg_parser = c_parser.messagesParser()
    #dir_monitor = monitor.DirectoryMonitor()
    #proc_monitor = monitor.ProcessMonitor()
    #metric_monitor = monitor.MetricsMonitor()
    
    #grabs list of all valid messages in regards to set schema
    messages = msg_parser.messages
    

    while True:
	print(messages)






