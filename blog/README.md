Installing KEDA through Helm:
```shell
helm repo add kedacore https://kedacore.github.io/charts
helm repo update
kubectl create namespace keda
helm install keda kedacore/keda --namespace abc --create-namespace
```

Setting up Authentication with Workload Identity:

* Creating GCP Service Account and IAM Binding
    ```shell
    SERVICE_ACCOUNT_NAME=gcppubsubtest
    PROJECT_ID=$(gcloud config get-value project)
    SERVICE_ACCOUNT_FULL_NAME=$SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com


    gcloud beta iam service-accounts create $SERVICE_ACCOUNT_NAME  --display-name "KEDA PubSub Sample"

    gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member serviceAccount:$SERVICE_ACCOUNT_FULL_NAME \
    --role roles/monitoring.viewer
    ```
* Binding GCP IAM Service Account and k8s service account 
    ```shell
    gcloud iam service-accounts add-iam-policy-binding $SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com \
    --role roles/iam.workloadIdentityUser \
    --member "serviceAccount:$PROJECT_ID.svc.id.goog[keda/keda-operator]"

    kubectl annotate serviceaccount keda-operator \
    --namespace keda \
    iam.gke.io/gcp-service-account=$SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com
    ```
* Creating Pub Sub Topic and Subscription
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