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
	    print("Focus mapping issue with: " + focus + " in: " +  monitor_type + " type message.")
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
	
    def results(self, message_object):

	results = {}
	print("NICE")

	return results


'''Interface for handling aggregation of lower and higher level aggregations
	configured for each message'''
class Aggregator(object):
    def __init__(self):
	self.test = 5

    def results(self, monitored_message):
	
	agg_results = {}

	msg_low_agg_results = self.get_lower_level_results(monitored_message.monitored_payload, monitored_message.low_level_aggs)
	msg_high_agg_results = self.get_high_level_results(msg_low_agg_results, monitored_message.high_level_aggs)

	agg_results.update(msg_low_agg_results)
	agg_results.update(msg_high_agg_results)

	return agg_results

    '''Gets the results of the lower level aggregations for use by possible 
	higher level aggregations.'''
    def get_lower_level_results(self, monitor_results, message_lower_aggs):
	
        total_count = {"1": 0, "2":0, "3":0, "4":0}
	lower_level_results = {}


	'''STATUS'''
	for monitor_result in monitor_results["status"]:
	    for low_agg in message_lower_aggs["status"]:
		print("LOW AGG  " + low_agg)
		for monitored_metric in message_lower_aggs["status"][low_agg]:
		    if monitored_metric == monitor_result:
		        total_count = self.status_check(total_count, monitored_metric, monitor_results["status"][monitor_result], message_lower_aggs["status"])	
			
	'''THRESHOLD'''
	for monitor_result in monitor_results["threshold"]:
	    for low_agg in message_lower_aggs["threshold"]:
		for monitored_metric in message_lower_aggs["threshold"][low_agg]:
		    if monitored_metric == monitor_result:
		        total_count = self.threshold_check(self.get_compare_type(), total_count, monitor_results["threshold"][monitor_result] , message_lower_aggs["threshold"])

			#lower_level_results[monitored_metric] = self.threshold_check(self.get_compare_type(
	
	return lower_level_results


    def get_compare_type(self, thresh_element):

       if thresh_element["healthy"] > thresh_element["warning"] and thresh_element["warning"] > thresh_element["critical"]:
           return 'decreasing'
       else:
           return 'increasing'

    def status_check(self, total_count, status_element_name, status_element_value, status_mapped_health):

        if status_element_value == status_mapped_health['healthy'][status_element_name]:
            total_count["2"] += 1
        elif status_element_value  == status_mapped_health['warning'][status_element_name]:
            total_count["3"] += 1
        elif status_element_value == status_mapped_health['failure'][status_element_name]:
            total_count["4"] += 1
        else:
            total_count["1"] += 1

        return total_count

    def threshold_check(self, compare_type, total_count, thresh_element, thresh_mapped_health):
       
	if compare_type == 'decreasing':
            if thresh_element > thresh_mapped_health['healthy']:
                total_count["2"] += 1
            elif (thresh_element  < thresh_mapped_health['healthy']) and (thresh_element > thresh_mapped_health['critical']):
                total_count["3"] += 1

            else:
                total_count["4"] += 1

        else:
            if thresh_element > thresh_mapped_health['critical']:
                total_count["4"] += 1
            elif (thresh_element > thresh_mapped_health['healthy']) and (thresh_element < thresh_mapped_health['critical']):
                total_count["3"] += 1

            else:
                total_count["2"] += 1

        return total_count





    #def get_status_result(self,

    def get_higher_level_results(self, lower_level_results, message_aggs):
	return higher_level_results


test = Monitor()
test_focus_dict = {"file_date": {"path": "./endpoint.py"}}


print(test.custom_sys_command(test_focus_dict, "directory"))


test_focus_dict = {"snmp_int_result":{"OID": "1.3.6.1.4.1.232.6.2.6.8.1.4.1.9"}}
print(test.custom_sys_command(test_focus_dict, "metric"))

test_focus_dict = {"snmp_string_result":{"OID": "1.3.6.1.4.1.2021.10.1.3.1"}}
print(test.custom_sys_command(test_focus_dict, "metric"))

