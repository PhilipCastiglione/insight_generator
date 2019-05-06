#!/bin/bash -ex

cd "$(dirname "$0")"

pip install -r requirements.txt

python import_deps.py

# TODO: check/establish creds for storage?

timestamp="$(date "+%Y%m%d_%H%M%S")"
echo $timestamp
# TODO: remove this; just a smaller dataset for testing
external_source_path="http://data.insideairbnb.com/australia/wa/western-australia/2019-03-07/data/reviews.csv.gz"
#external_source_path="http://data.insideairbnb.com/united-states/ny/new-york-city/2019-03-06/data/reviews.csv.gz"
source_data_path="gs://217157862preprocessing/sequential/$(timestamp)/source_data.csv"
cleaned_data_path="gs://217157862preprocessing/sequential/$(timestamp)/cleaned_data.csv"
preprocessed_data_path="gs://217157862preprocessing/sequential/$(timestamp)/preprocessed_data.csv"

curl $external_source_path \
  | tar --to-stdout -zxf -
  | gsutil cp - $source_data_path

gsutil cp - $source_data_path - \
  | python clean_data.py \
  | gsutil cp - $cleaned_data_path

gsutil cp - $cleaned_data_path - \
  | python preprocess_data.py \
  | gsutil cp - $preprocessed_data_path

# TODO: need some kind of web deployed accessible thing for the assignment
# TODO: echo the url
