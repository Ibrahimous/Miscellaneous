# -*- encoding: UTF-8 -*-

### Get a list tor nodes ###
## Written by @Ibrahimous ##

import requests, re, ConfigParser, sys

proxies = {
  "http": "http://<login>:<password>@<yourdomain>:<port>",
  "https": "http://<login>:<password>@<yourdomain>:<port>",
}

def printErr(err, str):
	"""Commodity function to display errors while fetching things"""

	print "Error fetching {}:".format(str), err
	sys.exit(1)

def get_url(url, bssl):
	"""
	Issues a get request to <url>, verify SSL certificates or not, based on <bssl>
	Return the response's body
	"""

	print "Issuing get request to:", url
	try:
		r = requests.get(url, verify=bssl)
		#OR r = requests.get(url, verify=bssl, proxies=proxies)
		print "Get request successful"
		req_status = r.status_code
		if req_status == 200:
			return r.text
		else:
			print "status code = {}".format(req_status)
	except:
		printErr(sys.exc_info()[0], url)

#FIXME: missing the "/" fucks things
def get_remote_rep_rev(rep_serv, bssl):
	"""Get the latest data's revision number from the reputation server"""

	print "Getting revision number..."
	try:
		#Get #https://reputation.alienvault.com/reputation.rev
		rev = get_url("{}reputation.rev".format(rep_serv), bssl)
		print "Got revision:", rev
		return rev
	except:
		printErr(sys.exc_info()[0], "revision")

def download_reputation_database(rep_serv, bssl):
	"""Get the latest data from the reputation server"""

	print "Getting data..."
	try:
		data = get_url("{}".format(rep_serv), bssl)
		print "Got data"
		return data
	except:
		printErr(sys.exc_info()[0], "data")


def check_reputation_format(line):
	"""Verifies the format of the data received"""

	r = re.compile("^[+-]?\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}#\d\d?#\d\d?#.*#.*#.*#.*#.*$")
	if line != "":
		if not r.match(line):
			return False
	return True


def parseData(data):
	for d in data.split("\n"):
		if check_reputation_format(d) and d != "":
			if d[0] == "-":
				continue
			if d[0] == "+":
				d = d[1:]
			fs = d.split("#") #<IP>#rel?#priority#Scanning Host#Country Code#City Name#<IP>#Lat Long
			#if len(fs) == 8:


if __name__ == '__main__':
	rep_serv = "https://www.dan.me.uk/torlist"
	#rev = get_remote_rep_rev(rep_serv, False)
	data = download_reputation_database(rep_serv, False)
	feedsFile = "tor_nodes"
	with open(feedsFile, 'w+') as f:
		f.write(data)
		print "Data written successfully to:", feedsFile

