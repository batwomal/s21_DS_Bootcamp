#!/bin/sh

echo "running partitioner.sh"

rm -f hh_positions_*.csv

input_file="../ex03/hh_positions.csv"
header=$(head -n 1 "$input_file")

awk -F',' -v header="$header" '
NR > 1 {
    date = substr($2, 1, 10)
    filename = "hh_positions_" date ".csv"
    if (!files[filename]++) {
        print header > filename
    }
    print $0 >> filename
}' "$input_file"