Creating GKE Cluster with Workload Identity enabled:
```shell
gcloud container clusters create demo-cluster --workload-pool=PROJECT_ID.svc.id.goog --workload-metadata=GKE_METADATA --machine-type=e2-medium --max-nodes=2 --zone us-central1-a
```

Installing KEDA through Helm:
```shell
helm repo add kedacore https://kedacore.github.io/charts
helm repo update
helm install keda kedacore/keda --namespace keda --create-namespace
```

Setting up Authentication with Workload Identity:

* Creating GCP Service Account and IAM Binding
    ```shell
    SERVICE_ACCOUNT_NAME=keda-gcppubsubtest
    PROJECT_ID=$(gcloud config get-value project)
    SERVICE_ACCOUNT_FULL_NAME=$SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com


    gcloud beta iam service-accounts create $SERVICE_ACCOUNT_NAME  --display-name "KEDA PubSub Sample"

    gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member serviceAccount:$SERVICE_ACCOUNT_FULL_NAME \
    --role roles/monitoring.viewer

    gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member serviceAccount:$SERVICE_ACCOUNT_FULL_NAME \
    --role roles/pubsub.subscriber
    ```
* Binding GCP IAM Service Account and k8s service account 
    ```shell
     gcloud iam service-accounts add-iam-policy-binding $SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com \
    --role roles/iam.workloadIdentityUser \
    --member "serviceAccount:$PROJECT_ID.svc.id.goog[keda/keda-operator]" \
    --member "serviceAccount:$PROJECT_ID.svc.id.goog[default/default]"

    kubectl annotate serviceaccount keda-operator \
    --namespace keda \
    iam.gke.io/gcp-service-account=$SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com


    #Access to consume pubsub messages from GKE Workloads
    gcloud iam service-accounts add-iam-policy-binding $SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com \
    --role roles/iam.workloadIdentityUser \
    --member "serviceAccount:$PROJECT_ID.svc.id.goog[default/default]"

    kubectl annotate serviceaccount default  \
    --namespace default \
    iam.gke.io/gcp-service-account=$SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com
    ```
Creating Pub Sub Topic and Subscription
```shell
SUBSCRIPTION_NAME=keda-test-subscription
TOPIC_NAME=keda-test-topic

gcloud beta pubsub topics create $TOPIC_NAME
gcloud beta pubsub subscriptions create $SUBSCRIPTION_NAME \
--topic $TOPIC_NAME

gcloud beta pubsub subscriptions add-iam-policy-binding $SUBSCRIPTION_NAME \
--member=serviceAccount:$SERVICE_ACCOUNT_FULL_NAME \
--role=roles/pubsub.subscriber
```