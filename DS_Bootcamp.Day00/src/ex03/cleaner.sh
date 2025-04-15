#!/bin/sh

echo "running cleaner.sh"

INPUT_FILE="../ex02/hh_sorted.csv"
OUTPUT_FILE="hh_positions.csv"

awk 'BEGIN { 
    FPAT = "([^,]+)|(\"[^\"]+\")"
    OFS = ","
}
NR == 1 {print $0; next}
{
    position = "-"
    if ($3 ~ /Junior/) position = "Junior"
    else if ($3 ~ /Middle/) position = "Middle"
    else if ($3 ~ /Senior/) position = "Senior"
    $3 = position
    print $0
}' "$INPUT_FILE" > "$OUTPUT_FILE"

