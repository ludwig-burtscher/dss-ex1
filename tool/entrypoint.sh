#!/bin/sh

mkdir -p /app/data/output/countries
mkdir -p /app/data/output/input_data
cp -r /app/data/raw/* /app/data/output/input_data
cat /app/VERSION > /app/data/output/TOOL_VERSION

python /app/preprocess.py /app/data/raw/COVID-19/$COVID_FILENAME /app/data/raw/Gold/$GOLD_FILENAME $START_DATE $END_DATE
python /app/visualize.py ./preprocessed.csv /app/data/output/countries