for x in {1..20}
do
gcloud beta pubsub topics publish keda-test-topic \
  --message "Test Message ${x}"
done
