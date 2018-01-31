import commands
import time
import logging
import json
import os


class snmpInterface(object):
    def __init__(self):

        self._snmpHost = ''
        self._snmpCommunity = ''
        self._snmpPort = 0

        #setting of declared snmp values
        self.setUpSNMP()




    def setUpSNMP(self):

        cwd = os.getcwd()
        try:
            with open(cwd + '/Config/generalConfig.json') as config:
                configDict = json.load(config)
        except:
            print('/nError loading generalConfig.json.')
            return


        try:
            self._snmpHost = configDict['SNMP']['host']
            self._snmpCommunity = configDict['SNMP']['community']
            self.snmpPort = configDict['SNMP']['port']
            self._snmpVersion = configDict['SNMP']['version']
        except:
            print('Error parsing SNMP data in generalConfig.json.')
            return

    def getSnmpResult(self, snmp_value):
        try:
            status, result = commands.getstatusoutput("snmpget -OUvs -" + self._snmpVersion + " -c"
                                                     + self._snmpCommunity + " "
                                                     + self._snmpHost + " "
                                                     + str(snmp_value))

        except:
            print('SNMP command failed.')

        return result.split(':',1)[1]


test = snmpInterface()

value = test.getSnmpResult('dskAvail.1')
print(value)
