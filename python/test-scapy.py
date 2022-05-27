import os, sys

if os.getuid() != 0:
	print "You must be root to launch this script, too bad"
	exit(-1)

if len(sys.argv) != 2:
	print "Usage: sudo python test-scapy.py <IP/network>"
	exit(-1)

from scapy.all import *

mon_ping = IP(dst=Net(sys.argv[1])) / ICMP()
# https://en.wikipedia.org/wiki/Internet_Control_Message_Protocol#Control_messages
# mon_ping.type = 8 <=> #echo-request

answered, unanswered = sr(mon_ping, timeout=0.5)

answering_IPs = []
unanswering_IPs = []

print "Answered requests: "
print "Issued request: "
for i in answered:
	# i = tuple
	# Add IP to list of answered
	for j in i:
		#print j.show()
		if j.type == 0:
			#echo-reply
			answering_IPs.append(j.dst)

print "Unanswered requests: "
print "Issued request: "
for i in unanswered:
	#Add ip to list of unanswered
	for j in i:
		unanswering_IPs.append(j.dst)

print answering_IPs
print unanswering_IPs
