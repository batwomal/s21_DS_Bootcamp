#!/bin/sh

if [ -z "$VIRTUAL_ENV" ]; then
  echo "The virtual environment is not active. Please activate it."
  exit 1
fi

pip install termgraph

termgraph data.txt --color red blue 