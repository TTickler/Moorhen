import c_parser
import os
import ConfigParser

#subprocess module is used here in place of sys to avoid overhead and be more pythonic 
import subprocess

'''Parent class of specialized monitors for directories, processes, and metrics'''
class Monitor(object):
    def __init__(self):

	#empty object to be overriten by children interfaces
	#used in exec_local(), but unique mappings are available for each child
	#ex would be MetricMonitor having functionality for getting SNMP query results 
        self._mappings = {} 

    @property 
    def monitor_type(self):
        return self._monitor_type

    @monitor_type.setter
    def monitor_type(self, monitor_type):
        self._monitor_type = monitor_type


    '''Uses focus mappings specific to each message to attempt to 
	make a valid system call, mapped in /Config/monitorMappings.ini, 
	and gather the results for the system call.


	focus_dict is the focus and its nested fields/values.'''
    def custom_sys_command(self, focus_dict, monitor_type):
	
	monitor_mapping_cfg = ConfigParser.ConfigParser()
	monitor_mapping_cfg.read(os.getcwd() + "/Config/monitorMappings.ini")
	
	try:
	    unparsed_cmd = monitor_mapping_cfg.get(monitor_type, focus)

	except:
	    print("Focus mapping issue with: " + focus + " in: " +  monitor_type + " type message.")
	    cmd_results = "FAILED PARSING FOCUS"

	cmd_results = ""

	for focus_mapping in focus_mappings:
	    if focus in 
	    

	return {"": cmd_results}

    def sys_command(self, command):
        
	try:
            command_result = subprocess.check_output([command])

	except:
	    print("Invalid System Command...")
	return command_result  

    def exec_local(self, focus_string):
	
	try:
	   self._mappings[focus_string]()

	except:
	   print(focus_string +  " is not a valid focus...") 
	

'''Child class of Monitor. Focuses on handling monitoring a directory'''
class DirectoryMonitor(Monitor):
    def __init__(self):
        Monitor.__init__(self)


	'''Mappings for function calls. This allows shipper's main to '''
        self._mappings = { 




                        }

    #def get_largest_file(self): 


'''Child class of Monitor. Focuses on handling monitoring metrics'''
class MetricMonitor(Monitor):
    def __init__(self):
        Monitor.__init__(self)

        self._mappings = { 
			   "get_snmp_results": self.get_snmp_results

                        }


    def get_snmp_results(self):
	print("THIS IS GET_SNMP_RESULTS()")



'''Child class of Monitor. Focuses on handling monitoring a process'''
class ProcessMonitor(Monitor):
    def __init__(self):
        Monitor.__init__(self)
	
	self._mappings = { 
			   "get_mem_used": self.get_mem_used,
			   "get_cpu_used": self.get_cpu_used,
			   "get_pid_by_name": self.get_pid_by_name
			}

    def get_pid_by_name(self, proc_name):
	
	PID = ''
	try:
            PID = subprocess.check_output(["pidof " + proc_name])
	except:
	    print("Invalid process name. Failed to retreive process ID.")

	return PID

    def get_mem_used(self):
	print("THIS IS GET_MEM_USED()")

    def get_cpu_used(self):
	print("THIS IS GET_CPU_USED()")



test = ProcessMonitor()

print(test.sys_command("ls"))
test.exec_local("get_cpu_used")
test.exec_local("get_mem_used")
#print(test.get_pid_by_name("java"))
