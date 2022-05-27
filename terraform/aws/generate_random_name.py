#!/usr/bin/env python
# -*- coding: utf-8 -*-

from string import ascii_lowercase
from random import choice

choice_range = ascii_lowercase
random_string_length = 12

output = ""

for x in range(random_string_length):
	output = output + choice(choice_range)

print(output)