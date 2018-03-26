import c_parser
import os
import sys

'''Parent class of specialized monitors for directories, processes, and metrics'''
class Monitor(object):
    def __init__(self):
        self.test = 5

    @property 
    def monitor_type(self):
        return self._monitor_type

    @type.setter
    def monitor_type(self, monitor_type):
        self._monitor_type = monitor_type  

'''Child class of Monitor. Focuses on handling monitoring a directory'''
class DirectoryMonitor(Monitor):
    def __init__(self):
        Monitor.__init__(self)

    def 


'''Child class of Monitor. Focuses on handling monitoring metrics'''
class MetricMonitor(Monitor):
    def __init__(self):
        Monitor.__init__(self)

'''Child class of Monitor. Focuses on handling monitoring a process'''
class ProcessMonitor(Monitor):
    def __init__(self, process_message):
        Monitor.__init__(self)
	

    def get_mem_used(self):
    def get_cpu_used(self):
