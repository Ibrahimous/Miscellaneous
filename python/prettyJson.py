#!/usr/bin/python
# -*-coding: utf-8 -*

import sys, json

## Working example (note the signle or double quotes): ##
# python prettyJson.py '{"person":{"mappings":"1"}}'

if __name__ == '__main__':
	try:
		js = json.loads(sys.argv[1])
		#print jsFile
		#If sort_keys is True (default: False), then the output of dictionaries will be sorted by key.
		print json.dumps(js, sort_keys=False, indent=2, separators=(',', ': '))
	except IndexError as ie:
		print "Usage: python prettyJson '<json data>'"
		exit(1)