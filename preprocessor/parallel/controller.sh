#!/bin/bash -ex

cd "$(dirname "$0")"

echo "commencing: $(date "+%Y%m%d_%H%M%S")" >> measurement.txt

export TIMESTAMP=$1
export BUCKET_NAME=$2
export INSTANCE_NUMBER=$3
export SCALE=$4
export SOURCE_DATA="gs://$BUCKET_NAME/reviews.csv"
export CLEANED_DATA="gs://$BUCKET_NAME/$TIMESTAMP/cleaned_data_$INSTANCE_NUMBER.csv"
export PREPROCESSED_DATA="gs://$BUCKET_NAME/$TIMESTAMP/preprocessed_data_$INSTANCE_NUMBER.csv"
export MEASUREMENTS="gs://$BUCKET_NAME/$TIMESTAMP/measurement_$INSTANCE_NUMBER.txt"

sudo apt install python3 python3-distutils
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py --user
~/.local/bin/pip3 install --user -r requirements.txt

python3 import_deps.py

gsutil cp $SOURCE_DATA reviews.csv

echo "finished setup: $(date "+%Y%m%d_%H%M%S")" >> measurement.txt

python3 clean_data.py reviews.csv cleaned_data.csv $INSTANCE_NUMBER $SCALE

echo "finished cleaning data: $(date "+%Y%m%d_%H%M%S")" >> measurement.txt

python3 preprocess_data.py cleaned_data.csv preprocessed_data.csv

echo "finished preprocessing data: $(date "+%Y%m%d_%H%M%S")" >> measurement.txt

gsutil cp cleaned_data.csv $CLEANED_DATA
gsutil cp preprocessed_data.csv $PREPROCESSED_DATA

echo "finished transferring data: $(date "+%Y%m%d_%H%M%S")" >> measurement.txt

# TODO: will need to rejoin files if we are the last to finish

gsutil cp measurement.txt $MEASUREMENTS

