#!/bin/sh

python /app/preprocess.py /app/data/raw/$COVID_FILENAME /app/data/raw/$GOLD_FILENAME $START_DATE $END_DATE
python /app/visualize.py ./preprocessed.csv /app/data/output/