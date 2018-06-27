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
    def custom_sys_command(self, focus , focus_type):
	
	monitor_mapping_cfg = ConfigParser.ConfigParser()
	monitor_mapping_cfg.read(os.getcwd() + "/Config/monitorMappings.ini")

	'''Uses Python's ConfigParser to parse mapping.
		Ex. If 'snmp_result was passed in for type metric the 
		unparsed_cmd would result in the string mapped to 
		'snmp_result under the metric category in monitorMappings.ini' ' '''
	
	focus_command = focus["command"]
	focus_name = focus["name"]
	
	try:
	    unparsed_cmd = monitor_mapping_cfg.get("commands", focus_command)

	except:
	    print("Focus mapping issue with: " + focus_command + " in: commands")
	    return "FAILED PARSING FOCUS"

	cmd_results = ""
	
	total_mappings = len(focus["mappings"].keys())

	if total_mappings != 0:
	    for mapping in focus["mappings"]:
	    	
	        #unparsed strings in monitorMappings.ini are {STRING} format
	        match_string = "{" + mapping  + "}"
		
	        if match_string in unparsed_cmd:
                    parsed_cmd = unparsed_cmd.replace(match_string, focus["mappings"][mapping])
	
	else:
	    #parsed_cmd becomes original unparsed_cmd due to no mappings
	    #meaning command was intended as is without any mappings
	    parsed_cmd = unparsed_cmd
	   	
	cmd_results = self.sys_command(parsed_cmd)
	
	return {focus_name: cmd_results}

    def sys_command(self, command):
        
	#args = shlex.split(command)
	#gets output from system call with a shell. Strips away \n character

	try:
            command_result = subprocess.check_output(command, shell=True).strip()
	except:
	    print("Command: " + str(command) + "failed. Result for command will be 0.")
	    command_result = 0
	return command_result  

    def exec_local(self, focus_string):
	
	try:
	   self._mappings[focus_string]()

	except:
	   print(focus_string +  " is not a valid focus...") 
	
    def results(self, message_object):

	results = {"status": [], "threshold": []}

	for focus in message_object.focus:

	    if focus["type"] == "status":
		results["status"].append(self.custom_sys_command(focus, "status")) 
	    else:
		results["threshold"].append(self.custom_sys_command(focus, "threshold"))
	
	return results


'''Interface for handling aggregation of lower and higher level aggregations
	configured for each message'''
class Aggregator(object):
    def __init__(self):
	self.test = 5

    def results(self, monitored_message):
	
	agg_results = {}

	msg_low_agg_results = self.get_lower_level_results(monitored_message.monitored_payload, monitored_message.low_level_aggs)
	msg_high_agg_results = self.get_higher_level_results(msg_low_agg_results, monitored_message.high_level_aggs)

	agg_results.update(msg_low_agg_results)
	agg_results.update(msg_high_agg_results)

	print("lower: " + str(msg_low_agg_results))

	#print(agg_results)
	return agg_results

    '''Gets the results of the lower level aggregations for use by possible 
	higher level aggregations.'''
    def get_lower_level_results(self, monitor_results, message_lower_aggs):
	
        total_count = {"1": 0, "2":0, "3":0, "4":0}
	lower_level_results = {}
	lower_level_agg_count = {}

	'''STATUS'''
	for monitor_result in monitor_results["status"]:
	    found = False
	    for monitor_result_name in monitor_result:
                #lower_level_agg_count[low_agg] = {"1": 0,"2": 0,"3": 0,"4": 0}

		#print("monitor_result: " + str(monitor_result) + " mon result name: " + monitor_result_name)
	        for low_agg in message_lower_aggs:
		    if low_agg in lower_level_agg_count.keys():
		        if lower_level_agg_count[low_agg] == total_count:
                            lower_level_agg_count[low_agg] = {"1": 0,"2": 0,"3": 0,"4": 0}
		    else:
			lower_level_agg_count[low_agg] = {"1": 0,"2": 0,"3": 0,"4": 0}
		    for health in message_lower_aggs[low_agg]["status"]:
			if found == True:
			    continue
		        if monitor_result_name in message_lower_aggs[low_agg]["status"][health]:
		            lower_level_agg_count[low_agg] = self.status_check(lower_level_agg_count[low_agg], monitor_result_name, monitor_result[monitor_result_name], message_lower_aggs[low_agg]["status"])
			    found = True

			else:
			    continue
			
	'''THRESHOLD'''
	
	#try:
	for monitor_result in monitor_results["threshold"]:
	    found = False
	    
	    for monitor_result_name in monitor_result:
	        for low_agg in message_lower_aggs:
		   
	            for metric in message_lower_aggs[low_agg]["threshold"]:
			if found == True:
			    continue

	                if metric in monitor_result:
			    
		            found = True
                            
	                    lower_level_agg_count[low_agg] = self.threshold_check(self.get_compare_type(message_lower_aggs[low_agg]["threshold"][metric]), lower_level_agg_count[low_agg], monitor_result[monitor_result_name], message_lower_aggs[low_agg]["threshold"][metric]) 
			    print("LOW LEVEL AGG: " + str(lower_level_agg_count))
			else:
			    continue
	#except:
	    #print("Error parsing threshold metrics. Check your messages configuration")	
		#lower_level_results[monitored_metric] = self.threshold_check(self.get_compare_type(

	#print(monitor_results)
	#print(lower_level_agg_count)	
	for lower_agg in lower_level_agg_count:
	    lower_level_results[lower_agg] = self.get_health(lower_level_agg_count[lower_agg])
		
	return lower_level_results

    def get_health(self, total_count):

        if total_count["4"] != 0:
            status = 4
        elif total_count["4"] == 0 and total_count["3"] != 0:
            status = 3
        else:
            status = 2

	return status

    def get_compare_type(self, thresh_element):

       if thresh_element["healthy"] > thresh_element["warning"] and thresh_element["warning"] > thresh_element["critical"]:
           return 'decreasing'
       else:
           return 'increasing'

    def status_check(self, total_count, status_element_name, status_element_value, status_mapped_health):

	#print("stat_element_name: " + str(status_element_name))
	#print(repr(status_element_value))	
	if str(status_element_value) == str(status_mapped_health["healthy"][status_element_name]):
            total_count["2"] += 1
        elif str(status_element_value)  == str(status_mapped_health['warning'][status_element_name]):
            total_count["3"] += 1
        elif str(status_element_value) == str(status_mapped_health['critical'][status_element_name]):
            print("stat_element_name: " + str(status_element_name))

            total_count["4"] += 1
        else:
            total_count["1"] += 1
#	print(str(status_element_name) + str(total_count))
        return total_count

    def threshold_check(self, compare_type, total_count, thresh_element_value, thresh_mapped_health):
      
	if compare_type == 'decreasing':
            if int(thresh_element_value) > thresh_mapped_health['healthy']:
                total_count["2"] += 1
            elif (int(thresh_element_value)  < thresh_mapped_health['healthy']) and (int(thresh_element_value) > thresh_mapped_health['critical']):
                total_count["3"] += 1

            else:
                total_count["4"] += 1
	
        else:
            if int(thresh_element_value) > thresh_mapped_health['critical']:
                total_count["4"] += 1
	
            elif (int(thresh_element_value) > thresh_mapped_health['healthy']) and (int(thresh_element_value) < thresh_mapped_health['critical']):
                total_count["3"] += 1

            else:
                total_count["2"] += 1
		
	

        return total_count





    #def get_status_result(self,

    def get_higher_level_results(self, lower_level_results, message_aggs):

	higher_level_results = {}
	higher_level_agg_count = {}

	for high_agg in message_aggs:
	    found = False
	    higher_level_agg_count[high_agg] = {"1": 0, "2": 0, "3": 0,"4": 0}
	    for health in message_aggs[high_agg]["status"]:
		if found == True:
		    continue
		for lower_level_result in lower_level_results:
		    
		    if lower_level_result in message_aggs[high_agg]["status"][health]:
			found = True
			higher_level_agg_count[high_agg] = self.status_check(higher_level_agg_count[high_agg], lower_level_result, lower_level_results[lower_level_result], message_aggs[high_agg]["status"])
		
		  		
        for high_agg in higher_level_agg_count:
            higher_level_results[high_agg] = self.get_health(higher_level_agg_count[high_agg])
	#print higher_level_results

	return higher_level_results


