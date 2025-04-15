#!/bin/sh

echo "running hh.sh"

API_URL="https://api.hh.ru/vacancies"

SEARCH_QUERY="data scientist"
PER_PAGE=20
PAGE=0

response=$(curl -G \
    --data-urlencode "text=$SEARCH_QUERY" \
    --data-urlencode "per_page=$PER_PAGE" \
    --data-urlencode "page=$PAGE" \
    "$API_URL")

echo "$response" | jq '.' > hh.json
