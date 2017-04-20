#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json, urllib2, sys


API = "http://api.gbif.org/v1/"


if (len(sys.argv) != 2):
    print('Please supply a file with dataset keys as the only argument')
    sys.exit(0)


with open(sys.argv[1]) as f:
    for key in f:
        d = json.load(urllib2.urlopen('{}dataset/{}'.format(API, key)))
        print(d['key'] + '\t' + d['type'] + '\t' + d['title'])

