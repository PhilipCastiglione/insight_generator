# PROVIDED VARS BY RUN SCRIPT:
#  * BUCKET_NAME
#  * START_LINE
#  * END_LINE
cd ~

export TARRED_CODE="parallel.tar.gz"
export SOURCE_CODE_PATH="gs://$BUCKET_NAME/$TARRED_CODE"

gsutil cp $SOURCE_CODE_PATH $TARRED_CODE

tar -xzf $TARRED_CODE

./sequential/controller.sh $BUCKET_NAME $START_LINE $END_LINE

