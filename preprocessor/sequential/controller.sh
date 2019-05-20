#!/bin/bash -ex

cd "$(dirname "$0")"

BUCKET_NAME=$1
TIMESTAMP="$(date "+%Y%m%d_%H%M%S")"
LOL_PATH="gs://$(BUCKET_NAME)/$(TIMESTAMP)/lol.csv"

echo lol > lol.csv

gsutil cp lol.csv $LOL_PATH
