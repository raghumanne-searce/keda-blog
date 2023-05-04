import os
from google.cloud import pubsub_v1

# Read project ID, topic name, and subscription name from environment variables
project_id = os.environ.get('PROJECT_ID')
topic_name = os.environ.get('TOPIC_NAME')
subscription_name = os.environ.get('SUBSCRIPTION_NAME')

# Set up Pub/Sub subscriber client and subscription path
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_name)

def callback(message):
    print(f'Received message: {message}')
    message.ack()

streaming_pull_future = subscriber.subscribe(
    subscription_path, callback=callback)
print(f'Listening for messages on {subscription_path}...')

with subscriber:
    try:
        streaming_pull_future.result()
    except Exception as ex:
        streaming_pull_future.cancel()
        print(f'Error while consuming messages: {ex}')