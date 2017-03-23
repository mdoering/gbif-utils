import json
import csv
import urllib2
from collections import namedtuple


API = "http://api.gbif.org/v1/"
LIMIT = 1000


data = urllib2.urlopen('{}occurrence/search?limit=0&facet=publishingOrg&publishingOrg.facetLimit={}&publishingOrg.facetOffset=0'.format(API, LIMIT))
orgs = json.load(data, object_hook=lambda d: namedtuple('Facet', d.keys())(*d.values())).facets[0].counts

with open('publisher.tsv', 'wb') as f:
    writer = csv.writer(f, csv.excel_tab)
    writer.writerow(("key", "title", "country", "occurrences"))
    for o in orgs:
        org = json.load(urllib2.urlopen('{}organization/{}'.format(API, o.name)), object_hook=lambda d: namedtuple('Org', d.keys())(*d.values()))        
        writer.writerow((org.key, org.title.encode("utf-8"), getattr(org, 'country', ''), o.count))

