gcloud container clusters delete keda-demo-cluster --location us-central1-a
gcloud iam service-accounts delete $SERVICE_ACCOUNT_FULL_NAME
gcloud pubsub topics delete $TOPIC_NAME
gcloud pubsub subscriptions delete $SUBSCRIPTION_NAME