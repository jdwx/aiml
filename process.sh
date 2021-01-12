#!/bin/sh

Project=$1

##  Convert corpus text to JSON.
./text-to-jsonl.py "${Project}"

##  Build the word index.
./text-index.py "${Project}"

##  Convert words to keys.
./text-to-keys.py "${Project}"

##  Prepare the FastText input file.
./text-to-fasttext.py "${Project}"

##  Build the raw FastText embedding.
./text-embed.py "${Project}"

##  Prepare the FastText merge data.
./text-embed-merge-prep.py "${Project}"

##  Do the merge calculations.
./text-embed-merge-calc.py "${Project}"

##  Apply the merge calculations to build one cohesive embed.
./text-embed-merge-apply.py "${Project}"

##  Flatten the keys.
./text-flatten.py "${Project}"

##  Build the X-Y samples.
./text-perword-xy.py "${Project}"

##  Compile the TFRecords.
./text-compile.py "${Project}"

##  Build the model.
./text-model.py "${Project}"
