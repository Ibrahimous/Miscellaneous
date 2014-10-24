#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import xmlrpclib

if len(sys.argv) < 2:
    raise AttributeError("Missing Ikare VM's IP address, usage: python getScanInfos <IP>")

hostIp =  sys.argv[1]
login = "admin"
mdp = "admin"

#Connection to the server
server_url = "https://"+login+":"+login+"@"+hostIp+"/rpc2"
server = xmlrpclib.Server(server_url)

#Retrieves hosts vulnerabilities and organize them in an array
#See https://ikare.itrust.fr/doc/iklang.html for criteria syntax
#hostReq = server.host.find(['name == "{0}"'.format(hostIp)])

hostReq = server.host.find()
hostReqCount = hostReq['count']
if hostReqCount == 0:
    print 'No data found for the given IP address.'
    sys.exit(1);

else:
	for (i, host) in enumerate(hostReq['data']):
		print "---------------------------------"
		print "Host "+str(i)+" informations"
		print "---------------------------------"
		print host.get("fqdn")
		hostIP = host.get("name")
		print hostIP
		print host.get("cpe_title")

		# Retrieves host's vuln details
		try:
		    statReq = server.stat.get(host.get("id"))
		except:
		    #Handle incorrect id exception here
		    raise

		print ""
		print "Number of critical vulnerabilities: {0}".format(statReq.get("critical"))
		print "Number of high vulnerabilities: {0}".format(statReq.get("high"))
		print "Number of medium vulnerabilities: {0}".format(statReq.get("medium"))
		print "Number of low vulnerabilities: {0}".format(statReq.get("low"))
		print "";
		print "Grade: {0}/10".format(statReq.get("grade"))
		
		print "---------------------------------"
		hostVulns = server.host.getVulns(host.get("id"))
		print "Vulnerabilities details for "+hostIP
		print ""
		#print hostVulns['data']
		for (j, vuln) in enumerate(hostVulns['data']):
			print "---------------------------------"
			print vuln.get("name")
			print vuln.get("output")

		'''
		hostServices = server.host.getServices()
		print "hostServices"
		print hostServices
		'''


#From the IP & racktables, find the PO

#then build an email
