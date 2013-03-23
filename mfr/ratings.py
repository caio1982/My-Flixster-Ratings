#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Caio Begotti
# <caio1982@gmail.com>
# Public Domain

from requests import get
from simplejson import load
from sys import version_info

if version_info[0] < 3:
    from codecs import open as open

class Ratings():
    def __init__(self, userid, limit=100):
        if userid is None:
            raise KeyError("Username ID must be specified")
        # first chrome user-agent string available at useragentstring.com
        self.ua = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17"}
        self.url = "http://www.flixster.com/api/users/%s/movies/ratings" % userid
        self.payload = {"page": "1", "limit": limit}
        self._fetch()

    def _fetch(self):
        ret = get(self.url, params=self.payload, headers=self.ua)
        self.data = ret.text

    def write(self, output):
        if output is None:
            raise KeyError("An output must be specified when calling write()")
        with open(output, "w", "utf-8") as o:
            o.write(self.data)

    def read(self, input):
        if input is None:
            raise KeyError("An input filename must be specified")
        with open(input, "r", "utf-8") as i:
            data = load(i)
            i.close()
        return data
