#!/usr/bin/python

import os
import sys


def update_offset(offset):
    offset_file = open(os.path.expanduser('~') + "/Shipper/Shipper/custom_focuses/resources/audit_offset", "rw+")     
    offset_file.truncate()
    offset_file.write(str(offset))

    offset_file.close()

def get_offset():
    offset_file = open(os.path.expanduser('~') + "/Shipper/Shipper/custom_focuses/resources/audit_offset", "rw+") 

    offset = offset_file.readline()
    offset_file.close()
    return offset

def get_audit_log(file_object, offset):

    file_object.seek(int(offset))
    log_entry = file_object.readline()
    new_position = file_object.tell()
    
    update_offset(new_position)

    return log_entry

if __name__ == "__main__":
    
    file_object = open("/var/log/audit/audit.log", "rw+")
   # offset_file = open(os.getcwd() + "/resources/audit_offset", "rw+")    

    offset = get_offset()
    print(get_audit_log(file_object, offset))
    
