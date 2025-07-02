import boto3
import time

# Replace with your actual queue URL
queue_url = 'https://sqs.us-east-1.amazonaws.com/123456789012/number-queue'

# Connect to SQS
sqs = boto3.client('sqs', region_name='us-east-1')  # change region if needed

i = 1
while True:
    # Send message
    sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=str(i)
    )
    print(f"Sent: {i}")
    i += 1
    time.sleep(60)  # wait for 1 minute
