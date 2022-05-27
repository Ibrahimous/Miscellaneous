#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

"""
##################################################################################
## Writing triggered alerts to a file
## Greetings to seanelavelle.com - http://www.seanelavelle.com/2012/04/11/scripting-splunk-alerts-with-python
## Charles Ibrahim - @Ibrahimous
##################################################################################
"""

#/!\ python 2.6.6 => logging.debug written in LOWER CASE (VS 2.7, which enables upper case)

#TODO - parse alert fields to get only necessary info

import os, csv, gzip, time, logging, sys, re, json

logging.basicConfig(filename="/dz-siem/product/sz1/splunk/bin/scripts/alertToIndex.log", filemode="a", level=logging.DEBUG)
def logfield(field): logging.debug("Got {0}".format(field))

"""
We want to get:
• The alert's name - os.environ['SPLUNK_ARG_4']
• The date of the event that triggered the alert - THIS is hard stuff
• The security devices that rang and made the alert be triggered: depends of your architecture. We took the example of storing security devices logs in separate indexesLes équipements de sécurité dont les logs ont permis de détecter l'alerte
    => 1 security device <-> 1 index
• Attacking and victim IPs
 -> Get the IP in the alert !
  --> Parse the field names to get them !
  --> Check the "\d+\.\d+\.\d+\.\d+" format
"""

# Read the environment variables that Splunk has passed to us, among :
scriptName = os.environ['SPLUNK_ARG_0']
#numberEventsReturned = os.environ['SPLUNK_ARG_1']
#searchTerms = os.environ['SPLUNK_ARG_2']
queryString = os.environ['SPLUNK_ARG_3']
alert_name = os.environ['SPLUNK_ARG_4']
#triggerReason = os.environ['SPLUNK_ARG_5']
#browserUrl = os.environ['SPLUNK_ARG_6']
rawEventsFile = os.environ['SPLUNK_ARG_8']

def displaymatch(match):
        """ Commodity function for displaying regex match """
        if match is None:
                print "Match is None"
                return None
        else:
                print "Match: {0}, groups={1}".format(match.group(), match.groups())
                return 1

if __name__ == "__main__":
        scriptTime = time.strftime("%A %d %B %Y %H:%M:%S")
        logging.debug("alert_name: "+alert_name) #/!\ python 2.6.6 => debug written in LOWER CASE (VS 2.7, which enables upper case)
        logging.debug("rawEventsFile: "+rawEventsFile)
        logging.debug("queryString: "+queryString)

        # baseEvent is the actual event we want to log
        # some of its parameters can be factorized
        baseEvent={} #The Event we're actually going to write !
        baseEvent['alert_name']=alert_name

        # search index <-> triggered security device
        indexPattern = re.compile(r"index=\"?(\w+)\"?") #marche PAS
        match = indexPattern.search(queryString) # <-> rex field=queryString "index=(?<secDevice>\w+).*"
        if match:
            baseEvent['secDevice']=match.group(1) # Read doc here: https://docs.python.org/2/library/re.html#re.MatchObject
            print baseEvent
        else:
            print "queryString does not contain any index information !"

        #some of them MUST be initialized
        var = ['_time', 'src', 'ext_ip', 'int_ip', 'src_ip', 'dest_ip', 'c_ip']
        fieldNumbers = {}
        for v in var:
            fieldNumbers[v]=-1
        #{'_time': -1, 'ext_ip': -1, 'int_ip': -1, 'src_ip': -1, 'dest_ip': -1}
        
        baseEvent['_time']=scriptTime #baseEvent time defaults to script time
        #{'_time': scriptTime, 'ext_ip': -1, 'int_ip': -1, 'src_ip': -1, 'dest_ip': -1}

        try:
            with open('/tmp/splunk_alert_events', 'ab') as alertsLogFile:
                eventsFile = csv.reader(gzip.open(rawEventsFile, 'rb'))
                #Read the first line and parse column names: get and trim them !
                """
                Each line in eventsFile looks like:
                ['Country', 'ext_ip', 'int_ip', 'rule', 'count', 'values(proto)', 'values(alert.signature)', '_timediff', 'values(host_url)', '__mv_Country', '__mv_ext_ip', '__mv_int_ip', '__mv_rule', '__mv_count', '__mv_values(proto)', '__mv_values(alert.signature)', '__mv__timediff', '__mv_values(host_url)']
                ['EvilCountry', 'AA.YY.BB.XX', 'aa.bb.cc.dd', 'alert udp any any -> any 123 (msg:"ET DOS Possible NTP DDoS Inbound Frequent Un-Authed MON_LIST Requests IMPL 0x03"; content:"|00 03 2A|"; offset:1; depth:3; byte_test:1,!&,128,0; byte_test:1,&,4,0; byte_test:1,&,2,0; byte_test:1,&,1,0; threshold: type both,track by_dst,count 2,seconds 60; reference:url,www.symantec.com/connect/blogs/hackers-spend-christmas-break-launching-large-scale-ntp-reflection-attacks; classtype:attempted-dos; sid:2017919; rev:2;)', '2', 'UDP', 'ET DOS Possible NTP DDoS Inbound Frequent Un-Authed MON_LIST Requests IMPL 0x03', '', '', '', '', '', '', '', '', '', '', '']
                """

                i=0
                for line in eventsFile:
                    if i==0: #first line <-> fields names
                        i+=1 #we won't enter here anymore
                        k=0 #field number
                        for field in line:
                            #TODO: case _time / baseEvent[v]:  1428673373
                            if field in var:
                                logfield(field)
                                fieldNumbers[field]=k
                                #print "fieldNumbers[field]: ", fieldNumbers[field]
                            k+=1
                    else:
                        for v in var:
                            if fieldNumbers[v]!=-1:
                                baseEvent[v]=line[fieldNumbers[v]]
                                #print "baseEvent[v]: ",  baseEvent[v]
                        stringifiedEvent=""
                        for key in baseEvent:
                            stringifiedEvent+=str(key)+"="+str(baseEvent[key])+", "
                        #print stringifiedEvent
                        alertsLogFile.write(stringifiedEvent+'\n')
        except Exception, e:
            logging.debug(e)