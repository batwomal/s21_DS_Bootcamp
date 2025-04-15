#!/bin/sh

echo "running json_to_csv.sh"

JSON_FILE="../ex00/hh.json"
FILTER_FILE="filter.jq"
OUTPUT_CSV="hh.csv"

jq -f "$FILTER_FILE" "$JSON_FILE" | jq -r '(.[0] | keys_unsorted) as $keys | $keys, map([.[$keys[]]])[] | @csv' > "$OUTPUT_CSV"
