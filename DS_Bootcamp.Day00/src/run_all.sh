#!/bin/sh

cd ex00 && ./hh.sh
cd ../ex01 && ./json_to_csv.sh
cd ../ex02 && ./sorter.sh
cd ../ex03 && ./cleaner.sh
cd ../ex04 && ./counter.sh
cd ../ex05 && ./partitioner.sh 
./concatenator.sh
