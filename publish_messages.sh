for x in {1..20}
do
gcloud beta pubsub topics publish $TOPIC_NAME \
  --message "Test Message ${x}"
done