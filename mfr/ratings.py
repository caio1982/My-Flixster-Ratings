#!/usr/bin/env python
# -*- coding: utf-8 -*-
# public domain

"""
Fetches all ratings of a given user from Flixster.com,
writes it to a file in disk and reads it back.
"""

__author__ =  'Caio Begotti <caio1982@gmail.com>'

from requests import get
from simplejson import load
from unicodecsv import writer
from sys import version_info

if version_info[0] < 3:
    from codecs import open as open

class Ratings():
    """
    Class to fetch, read, save and export movies ratings from a Flixster.com account.
    """
    
    def __init__(self, userid, limit=100):
        """
        Constructor.

        @userid: required user code from Flixster.com.
        @limit: ratings limit to retrieve, defaults to 100.
        """
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
        """
        Writes all ratings to a JSON file.

        @output: required output filename.
        """
        if output is None:
            raise KeyError("An output must be specified when calling write()")
        with open(output, "w", "utf-8") as o:
            o.write(self.data)

    def read(self, input):
        """
        Reads a JSON file with ratings. Returns a JSON object.

        @input: required input filename.
        """
        if input is None:
            raise KeyError("An input filename must be specified")
        with open(input, "r", "utf-8") as i:
            data = load(i)
            i.close()
        return data

    def export(self, filename):
        """
        Export all ratings fetched to a CSV file. Entries marked as
        Want-To-See in Flixster will be saved with a zeroed score, entries
        marked as Not-Interested will be saved with score -1.

        As of now the CSV fields are:
            - Movie ID
            - Movie Title
            - Your rating
            - Rottent Tomatoes rating
            - Audience rating

        @filename: required name of the .csv file.
        """
        if filename is None:
            raise KeyError("A filename must be specified when exporting")
        with open(filename, "w") as f:
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
                csv.writerow(row)
