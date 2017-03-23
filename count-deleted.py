import json
import urllib2
import csv


API = "http://api.gbif.org/v1/"
SPECIES_FILE="deleted.txt"


occurrences=0
taxa=0


with open(SPECIES_FILE) as tsv:
    for line in csv.reader(tsv, delimiter='\t', quoting=csv.QUOTE_NONE):
        key=line[0]
        # phylumKey
        # rank
        # name
        cnt = urllib2.urlopen('{}occurrence/count?taxonKey={}'.format(API, key))
        if cnt > 0:
            print('{} occurrences found for {} {} [{}] phylum {}'.format(cnt, line[2], line[3], key, line[1]))

