# PROVIDED VARS BY RUN SCRIPT:
#  * BUCKET NAME
cd ~

export TARRED_CODE="sequential.tar.gz"
export SOURCE_CODE_PATH="gs://$BUCKET_NAME/$TARRED_CODE"

gsutil cp $SOURCE_CODE_PATH $TARRED_CODE

tar -xzf $TARRED_CODE

./sequential/controller.sh $BUCKET_NAME

