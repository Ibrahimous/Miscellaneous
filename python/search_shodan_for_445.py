#!/usr/bin/env python

import shodan
import sys

SHODAN_API_KEY = "XXXX_INSERT_YOUR_API_KEY_XXXXX"

api = shodan.Shodan(SHODAN_API_KEY)

querystr = sys.argv[1]
# querystr = "port:445 country:US"

# Wrap the request in a try/ except block to catch errors
try:
      # Search Shodan
      results = api.search(querystr)

      # Show the results
      print ('Results found: %s' % results['total'])
      for result in results['matches']:
          if 'SMB Version: 1' in result['data']:
              print ('IP: %s' % result['ip_str'])
              if 'os' in result:
                  print ('OS: %s' % result['os'])
              if 'devicetype' in result:
                  print ('Devicetype: %s' % result['devicetype'])
              if 'product' in result:
                  print ('Product: %s' % result['product'])
              if 'info' in result:
                  print ('Info: %s' % result['info'])
              print (result['data'])
              print ('')
except shodan.APIError as e:
      print ('Error: %s' % e)
