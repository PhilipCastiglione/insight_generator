#!/bin/bash -ex

cd "$(dirname "$0")"

export TIMESTAMP="$(date "+%Y%m%d_%H%M%S")"
echo "commencing: $TIMESTAMP" >> measurement.txt

export BUCKET_NAME=$1
export SOURCE_DATA="gs://$BUCKET_NAME/reviews.csv"
export CLEANED_DATA="gs://$BUCKET_NAME/$TIMESTAMP/cleaned_data.csv"
export PREPROCESSED_DATA="gs://$BUCKET_NAME/$TIMESTAMP/preprocessed_data.csv"
export MEASUREMENTS="gs://$BUCKET_NAME/$TIMESTAMP/measurement.txt"

sudo apt install python3 python3-distutils
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py --user
~/.local/bin/pip3 install --user -r requirements.txt

python3 import_deps.py

gsutil cp $SOURCE_DATA reviews.csv

echo "finished setup: $(date "+%Y%m%d_%H%M%S")" >> measurement.txt

python3 clean_data.py reviews.csv cleaned_data.csv

echo "finished cleaning data: $(date "+%Y%m%d_%H%M%S")" >> measurement.txt

python3 preprocess_data.py cleaned_data.csv preprocessed_data.csv

echo "finished preprocessing data: $(date "+%Y%m%d_%H%M%S")" >> measurement.txt

gsutil cp cleaned_data.csv $CLEANED_DATA
gsutil cp preprocessed_data.csv $PREPROCESSED_DATA

echo "finished transferring data: $(date "+%Y%m%d_%H%M%S")" >> measurement.txt

gsutil cp measurement.txt $MEASUREMENTS

