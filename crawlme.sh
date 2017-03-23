#!/bin/bash

API=http://api.gbif.org/v1
PASSWORD=xxx

for UUID in "$@"
do
    echo "crawl dataset:" $UUID
    curl --user markus:$PASSWORD -H "Content-Type: application/json" -H "Accept: application/json" -X POST $API/dataset/$UUID/crawl
done

