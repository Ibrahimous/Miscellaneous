#!/usr/bin/env python

import hashlib
import sys

if len(sys.argv) != 2:
	print "Usage: ./compute_md5.py <string>"
	exit(-1)

m = hashlib.md5()
print "Hash of", sys.argv[1], "is:" 

m.update(sys.argv[1])

print m.hexdigest()
