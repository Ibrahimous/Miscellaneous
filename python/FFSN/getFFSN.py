#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

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

def readConfFile(config_file):
    try:
            config = ConfigParser.RawConfigParser()
            config.read(config_file)
            print "Read config file successfully"
    except:
            print "Error reading config file:", sys.exc_info()[0]
            raise

def get_feeds(urlDict, bssl):
        """
        Issues a get request to <urlValue>, verify SSL certificates or not, based on <bssl>
        Return the response's body
        """

        for key, urlValue in urlDict.iteritems():
            print "Issuing get request to:", urlValue
            try:
                    r = requests.get(urlValue, verify=bssl, proxies=proxies)
                    req_status = r.status_code
                    if req_status == 200:
                        print "Get request successful"
                        feedFile=str(key)+".feed"
                        with open(feedFile, 'wb+') as f:
                            f.write(r.text)
                            print "Data written successfully to:", feedFile
                    else:
                        print "status code = {}".format(req_status)
            except Exception as err:
                print "Error fetching {}:".format(urlValue), err

#TODO : finish this !
def check_response(line):
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
        #A dictionnary containing the URLs to get FFSN info from
        urlDict={}
        """
        Palevo is a worm that spreads using instant messaging, P2P networks and removable drives (like USB sticks).
        """
        urlDict['palevo'] = "https://palevotracker.abuse.ch/blocklists.php?download=domainblocklist"

        """
        Well, you've heard of Zeus
        """
        urlDict['zeus'] = "https://zeustracker.abuse.ch/blocklist.php?download=domainblocklist"

        """
        Feodo (also known as Cridex or Bugat) is a Trojan used to commit ebanking fraud and steal sensitive information from the victims computer,
        such as credit card details or credentials.
        At the moment, Feodo Tracker is tracking four versions of Feodo, and they are labeled by Feodo Tracker as version A, version B, version C and version D.
        """
        urlDict['feodo'] = "https://feodotracker.abuse.ch/blocklist/?download=domainblocklist"

        get_feeds(urlDict, True)

