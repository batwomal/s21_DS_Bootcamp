#!/bin/sh

echo "running concatenator.sh"

rm -f result.csv

first_file=$(ls hh_positions_*.csv | head -n 1)
header=$(head -n 1 "$first_file")
echo "$header" > result.csv

for file in hh_positions_*.csv; do
    if [ -f "$file" ]; then
        tail -n +2 "$file" >> result.csv
    fi
done