import c_parser
import os, shlex, subprocess
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

	'''Uses Python's ConfigParser to parse mapping.
		Ex. If 'snmp_result was passed in for type metric the 
		unparsed_cmd would result in the string mapped to 
		'snmp_result under the metric category in monitorMappings.ini' ' '''

	for focus in focus_dict:
	    focus = focus
	
	try:
	    unparsed_cmd = monitor_mapping_cfg.get(monitor_type, focus)

	except:
	    print("Focus mapping issue with: " + "tsts" + " in: " +  monitor_type + " type message.")
	    return "FAILED PARSING FOCUS"

	cmd_results = ""

	for focus in focus_dict:
	    for mapping in focus_dict[focus]:
		
		#unparsed strings in monitorMappings.ini are {STRING} format
		match_string = "{" + mapping  + "}"
		
		if match_string in unparsed_cmd:
		    parsed_cmd = unparsed_cmd.replace(match_string, focus_dict[focus][mapping])

		else:
		    continue	
	cmd_results = self.sys_command(parsed_cmd)

	return {focus: cmd_results}

    def sys_command(self, command):
        
#	args = shlex.split(command)
        print(repr(command))
        command_result = subprocess.check_output(command, shell=True)
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



test = Monitor()
test_focus_dict = {"file_size": {"file": "./endpoint.py"}}


print(test.custom_sys_command(test_focus_dict, "directory"))


test_focus_dict = {"snmp_result":{"OID": "1.3.6.1.4.1.232.6.2.6.8.1.4.1.9"}}
print(test.custom_sys_command(test_focus_dict, "metric"))


