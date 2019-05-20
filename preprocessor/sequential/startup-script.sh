# PROVIDED VARS BY RUN SCRIPT:
#  * BUCKET NAME
# TODO: REMOVE
cat foo > foo.csv
gsutil cp foo.csv "gs://$(BUCKET_NAME)/foo.csv"

TARRED_CODE="sequential.tar.gz"
SOURCE_CODE_PATH="gs://$(BUCKET_NAME)/$(TARRED_CODE)"

gsutil cp $SOURCE_CODE_PATH $TARRED_CODE

tar -xzf $TARRED_CODE
# TODO: REMOVE
cat bar > bar.csv
gsutil cp bar.csv "gs://$(BUCKET_NAME)/bar.csv"

./sequential/controller.sh $BUCKET_NAME
# TODO: REMOVE
cat baz > baz.csv
gsutil cp baz.csv "gs://$(BUCKET_NAME)/baz.csv"
