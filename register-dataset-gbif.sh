#!/bin/bash

API=http://api.gbif.org/v1
PASSWORD=xxx
PUBLISHER=fbca90e3-8aed-48b1-84e3-369afbd000ce
INSTALLATION=5a914de7-822f-414c-b6ef-9a4874d717bb

for URL in "$@"
do
    echo "register endpoint:" $URL

    CONTENT="{\"type\": \"CHECKLIST\", \"title\": \"Placeholder title\", \"publishingOrganizationKey\":\"$PUBLISHER\", \"installationKey\":\"$INSTALLATION\"}"
    echo $CONTENT
    
    DATASET=$(curl --silent --user markus:carla1109 -H "Content-Type: application/json" -H "Accept: application/json" -X POST -d "$CONTENT" $API/dataset)
    # remove quotes
    DATASET=${DATASET%\"}
    DATASET=${DATASET#\"}
    echo "datasetKey: $DATASET"
    
    curl --silent --user markus:$PASSWORD -H "Content-Type: application/json" -H "Accept: application/json" -X POST -d "{\"type\":\"DWC_ARCHIVE\", \"url\":\"$URL\"}" $API/dataset/$DATASET/endpoint
done

