#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Caio Begotti
# <caio1982@gmail.com>
# Public Domain

from mfr import ratings

r = ratings.Ratings("845548311", 3)
backup = "myflixsterratings.json"

if r.write(backup):
    print "Ratings saved!"

data = r.read(backup)
print data
