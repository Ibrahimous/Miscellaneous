# -*- encoding: UTF-8 -*-

### Get a list of ip reputation from the alienvault database ###
## Inspired by: https://code.google.com/p/alienvault-labs-garage ##
## Written by @Ibrahimous ##

"""
TODO:
- add result parsing
- add data updating (VS downloading all the latest data)

+ merge with tor nodes
+  with http://rules.emergingthreats.net/
"""

import requests, re, ConfigParser, sys

proxies = {
  "http": "http://<login>:<password>@<yourdomain>:<port>",
  "https": "http://<login>:<password>@<yourdomain>:<port>",
}

config_file = "feeds.cfg"
try:
	config = ConfigParser.RawConfigParser()
	config.read(config_file)
	print "Read config file successfully"
except:
	print "Error reading config file:", sys.exc_info()[0]
	raise

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
"""
def get_remote_patch(rep_serv, revision):
	patch = get_url("%srevisions/reputation.data_%s" % (rep_serv, revision))
	rev = get_url("%sreputation.rev" % rep_serv)
	if rev != None:
		config.set('main', 'revision', rev)
		with open(config_file, 'wb') as configfile:
		    config.write(configfile)
	return patch
"""
def download_reputation_database(rep_serv, bssl):
	"""Get the latest data from the reputation server"""

	print "Getting data..."
	try:
		#Get #https://reputation.alienvault.com/reputation.data
		data = get_url("{}reputation.data".format(rep_serv), bssl)
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

def filterData(data):
	filtered_data = ""
	scanning_host = 0
	for d in data.split("\n"):
		#print d
		"""
		if check_reputation_format(d) and d != "":
			if d[0] == "-" or d[3] == "Scanning Host":
				continue
			if d[0] == "+":
				d = d[1:]
			fs = d.split("#") #<IP>#reliability#priority#Scanning Host#Country Code#City Name#Lat,Long#??
			filtered_data+=fs[0]+fs[3]+fs[4]+fs[5]+fs[6]+"\n" #<IP>#Scanning Host#Country Code#City Name#Lat,Long#??
		"""
		fs = d.split("#") #<IP>#reliability#priority#Scanning Host#Country Code#City Name#Lat,Long#??
		if len(fs)>3 and fs[3] == "Scanning Host":
			scanning_host+=1
			continue
		if len(fs)>6:
			new_line = fs[0]+"#"+fs[3]+"#"+fs[4]+"#"+fs[5]+"#"+fs[6]+"#"+"\n"
			filtered_data+= new_line #<IP>#Scanning Host#Country Code#City Name#Lat,Long#??
		else:
			print "end of data"
		#print new_line
	print str(scanning_host)+" Scanning Hosts weren't taken into account"
	return filtered_data

if __name__ == '__main__':
	rep_serv = config.get('main', 'reputation_server') #https://reputation.alienvault.com/
	rev = get_remote_rep_rev(rep_serv, False)
	raw_data = download_reputation_database(rep_serv, False)
	""" TRAITEMENT DES DONNÉES REÇUES """
	filtered_data = filterData(raw_data)
	feedsFile = "alienvault_feeds"
	with open(feedsFile, 'w+') as f:
		f.write(filtered_data)
		print "Data written successfully to:", feedsFile
