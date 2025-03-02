#!/bin/bash
set -e

# Wait for CouchDB to be ready
until curl -s http://couchdb:5984/ > /dev/null; do
    echo "Waiting for CouchDB to start..."
    sleep 1
done

# Create the database
curl -X PUT http://admin:cs233344@couchdb:5984/text_mpc

# Create indexes for better query performance
curl -X POST http://admin:cs233344@couchdb:5984/text_mpc/_index \
  -H "Content-Type: application/json" \
  -d '{
    "index": {
      "fields": ["content"]
    },
    "name": "content-index",
    "type": "json"
  }'

curl -X POST http://admin:cs233344@couchdb:5984/text_mpc/_index \
  -H "Content-Type: application/json" \
  -d '{
    "index": {
      "fields": ["tags"]
    },
    "name": "tags-index",
    "type": "json"
  }'

echo "CouchDB initialization completed."