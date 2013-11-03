#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Caio Begotti
# <caio1982@gmail.com>
# Public Domain

from mfr import ratings

# fetch ratings (first 100 by default)
r = ratings.Ratings("845548311", 9999)
backup = "myflixsterratings.json"

# write the json to a file
if r.write(backup):
    print "Ratings saved!"

# read the json from the file
data = r.read(backup)
print "Ratings data length is", len(data)

# export it to a real file
if r.export("dump.csv"):
    print "CSV file exported!"
