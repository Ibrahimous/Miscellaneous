#!/usr/bin/env python

## ANSSI Bonjour Twitter ##
# REF: https://twitter.com/ANSSI_FR/status/653539044148781056 #

import binascii

binList = ["01000010", "01101111", "01101110", "01101010", "01101111", "01110101", "01110010", "00100000", "01010100", "01110111", "01101001", "01110100", "01110100", "01100101", "01110010"]

str=""

for b in binList:
	n = int(b, 2)
	str += binascii.unhexlify('%x' % n)

print str
	

