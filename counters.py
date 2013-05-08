#!/usr/bin/env python2.7

# This script takes a text file containing a list of foods separated by 
# newlines, searches a corpus of "diet app" entries crowdsourced from Amazon
# Mechanical Turks, and outputs the counters (numbers and units) used in
# conjunction with each of the specified foods.
# Written by Tristan Euan Chong on 4/23/2013

import os
import re

# This file contains the list of foods for which to extract counters, separated
# by newlines
cat_file = 'categories.txt'

categories = [line.strip() for line in open(cat_file, 'r').readlines()]
#categories = cat_column.split('\n')

# This directory contains the "diet app" entries elicited from Turks
src_dir = 'data'

# This directory contains the output (counters per specified food)
des_dir = 'category_counters'

# Instantiate data structures
entries = []
counters = {}

# Split Turk data into individual food entries 
# i.e. "x, y, and z" -> ['x', 'y', 'z']
for filename in os.listdir(src_dir):
    for line in open(os.path.join(src_dir, filename), 'r').readlines():
                split = re.split(',| and ', line)
                for entry in split:
                    entries.append(entry.strip())

# Create empty list as a value for each key in dict
for category in categories:
    counters[category] = []

# Extract substrings preceding "of"
for entry in entries:
    of_count = entry.count(' of ')
    if of_count > 0:
        for category in categories:
            if category in entry:
                counters[category] += re.split(' of ', entry)[:of_count]

# Make sure destination path exists
if not os.path.exists(des_dir):
    os.makedirs(des_dir)

# Write counters to individual files corresponding to food names
for category in counters:
    if len(counters[category]) > 0:
        des_file = open(os.path.join(des_dir, '%s.txt' % category), 'w')
        des_file.write('\n'.join(counters[category]))
        des_file.close()
