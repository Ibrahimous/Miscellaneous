# -*- encoding: UTF-8 -*-

### Get opendns infos ###
## Written by @Ibrahimous ##

import requests, re, sys

proxies = {
  "http": "https://YOUR_SERVER_HERE:HTTP_PORT",
  "https": "https://YOUR_SERVER_HERE:HTTPS_PORT",
}

headers = {'Authorization': 'Bearer YOUR_TOKEN_HERE'}

def printErr(err, str):
	"""Commodity function to display errors while fetching things"""

	print "Error fetching {}:".format(str), err
	sys.exit(1)

def get_url(url, bssl):
	"""
	Issues a get request to <url>, verify SSL certificates or not, based on <bssl>
	Return the response's body
	"""

	print "Issuing GET request to:", url
	try:
		r = requests.get(url, verify=bssl, proxies=proxies, headers=headers)
		print "Get request successful"
		req_status = r.status_code
		if req_status == 200:
			print "Got data"
			return r.text
		else:
			print "status code = {}".format(req_status)
	except:
		printErr(sys.exc_info()[0], url)

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
			new_line = fs[0]+"#"+fs[1]+"#"+fs[2]+"#"+fs[3]+"#"+fs[4]+"#"+fs[5]+"#"+fs[6]+"#"+"\n"
			filtered_data+= new_line #<IP>#Scanning Host#Country Code#City Name#Lat,Long#??
		else:
			print "end of data"
		#print new_line
	print str(scanning_host)+" Scanning Hosts weren't taken into account"
	return filtered_data

if __name__ == '__main__':
	url = "https://investigate.api.opendns.com/dnsdb/name/a/example.com.json"
	bssl = False
	raw_data = get_url(url, bssl)
	#filtered_data = filterData(raw_data)
	feedsFile = "opendns_feeds"
	with open(feedsFile, 'w+') as f:
		#f.write(filtered_data)
		f.write(raw_data)
		print "Data written successfully to:", feedsFile
