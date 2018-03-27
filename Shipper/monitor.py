import c_parser
import os

#subprocess module is used here in place of sys to avoid overhead and be more pythonic 
import subprocess

'''Parent class of specialized monitors for directories, processes, and metrics'''
class Monitor(object):
    def __init__(self):
        self.test = 5

    @property 
    def monitor_type(self):
        return self._monitor_type

    @monitor_type.setter
    def monitor_type(self, monitor_type):
        self._monitor_type = monitor_type

    def sys_command(self, command):
        
	try:
            command_result = subprocess.check_output([command])

	except:
	    print("Invalid System Command...")
	return command_result  

'''Child class of Monitor. Focuses on handling monitoring a directory'''
class DirectoryMonitor(Monitor):
    def __init__(self):
        Monitor.__init__(self)

        self._mappings = { 




                        }



    #def get_largest_file(self): 


'''Child class of Monitor. Focuses on handling monitoring metrics'''
class MetricMonitor(Monitor):
    def __init__(self):
        Monitor.__init__(self)

        self._mappings = { 




                        }






'''Child class of Monitor. Focuses on handling monitoring a process'''
class ProcessMonitor(Monitor):
    def __init__(self, process_message):
        Monitor.__init__(self)
	
	self._mappings = { 




			}

    #def get_mem_used(self):
    #def get_cpu_used(self):



test = Monitor()

print(test.sys_command("ls"))
raw_in = raw_input()
print(globals())
