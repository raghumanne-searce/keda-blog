FROM python:3.9-slim-buster

# Install the required dependencies
RUN pip install --no-cache-dir google-cloud-pubsub==2.7.0 pytz

# Copy the Python script into the container
COPY consume_messages.py .

# Run the Python script
CMD ["python", "consume_messages.py"]