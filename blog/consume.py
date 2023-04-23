#This script is to consume the message from the topic
from google.cloud import pubsub_v1

# Prompt user to enter project ID, topic name, and subscription name
project_id = input("Enter your project ID: ")
topic_name = input("Enter the name of the topic: ")
subscription_name = input("Enter the name of the subscription: ")

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