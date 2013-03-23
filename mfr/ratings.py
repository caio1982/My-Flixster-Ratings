#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Caio Begotti
# <caio1982@gmail.com>
# Public Domain

from requests import get
from simplejson import load
from csv import writer
from sys import version_info

if version_info[0] < 3:
    from codecs import open as open

class Ratings():
    def __init__(self, userid, limit=100):
        if userid is None:
            raise KeyError("Username ID must be specified")
        # first chrome user-agent string available at useragentstring.com
        self.ua = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17"}
        # thanks https://github.com/mmihaljevic/flixter for the api address
        self.url = "http://www.flixster.com/api/users/%s/movies/ratings" % userid
        self.payload = {"page": "1", "limit": limit}
        self._fetch()

    def _fetch(self):
        ret = get(self.url, params=self.payload, headers=self.ua)
        self.data = ret.text
        self.json = ret.json

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

    def export(self, filename):
        if filename is None:
            raise KeyError("A filename must be specified when exporting")
        with open(filename, "w", "utf-8") as f:
            csv = writer(f)
            csv.writerow(["Id", "Movie", "Score", "Tomatometer", "Audience"])
            for entry in self.json:
                id = entry["movieId"]
                title = entry["movie"]["title"]

                # handles want-to-see and not-interested entries
                if "wts" in entry["scoreCss"]:
                    score = 0
                elif "ni" in entry["scoreCss"]:
                    score = -1
                else:
                    score = int(entry["scoreCss"])

                if "tomatometer" in entry["movie"]:
                    tomatoes = entry["movie"]["tomatometer"]
                else:
                    tomatoes = 0

                if "audienceScore" in entry["movie"]:
                    audience = entry["movie"]["audienceScore"]
                else:
                    audience = 0

                row = [id, title, score, tomatoes, audience]
                print row
                csv.writerow(row)
