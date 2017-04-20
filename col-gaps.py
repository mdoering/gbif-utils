from __future__ import division
import json
import urllib2


API = "http://api.gbif.org/v1/"
NUB= "d7dddbf4-2cf0-4f39-9b2a-bb099caae36c"
COL= "7ddf754f-d193-4cc9-b351-99906754a03b"
CUTOFF_NAMES = 50000
CHILD_LIMIT=1000

class Usage:
    """A name usage with metrics"""
    key = -1
    rank = ""
    name = ""
    indent = 0
    names = 0
    namesCol = 0

    def __init__(self, usageJson=None, key=None, indent=0):
        if key and not usageJson:
            usageJson = json.load(urllib2.urlopen('{}species/{}'.format(API, key)))
        self.indent = indent
        self.key = usageJson['key']
        self.rank = usageJson['rank']
        self.name = usageJson['scientificName']
        # rank=SPECIES
        result = json.load(urllib2.urlopen('{}species/search?limit=0&facet=constituentKey&dataset_key={}&highertaxon_key={}'.format(API, NUB, self.key)))
        self.names = result['count']
        for cnt in result['facets'][0]['counts']:
            if cnt['name'] == COL:
                self.namesCol = cnt['count']
        
    def __str__(self):
        return '{}:{} {}({})'.format(self.key, self.rank, self.name, self.names, self.namesCol, self.classification)

    def children(self):
        return [Usage(c, indent=self.indent+1) for c in json.load(urllib2.urlopen('{}species/{}/children?limit={}'.format(API, self.key, CHILD_LIMIT)))['results'] if c['numDescendants'] > CUTOFF_NAMES]

    def data(self):
        return '{}{} {} [{}] - {:.0%} {:,}'.format("  " * self.indent, self.rank, self.name, self.key, 0 if self.names == 0 else self.namesCol / self.names, self.names)


def walk(u):
    print(u.data())
    for c in u.children():
        walk(c)

# add root kingdoms
kingdoms=[Usage(key=kid) for kid in range(1,8)]

# update total
total = sum([k.names for k in kingdoms])
print('TOTAL names={}, CUTOFF={} names'.format(total, CUTOFF_NAMES))

# now walk each kingdom
for k in kingdoms:
    walk(k)

