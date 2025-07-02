import boto3

queue_url = 'https://sqs.us-east-1.amazonaws.com/123456789012/number-queue'

sqs = boto3.client('sqs', region_name='us-east-1')

while True:
    # Receive message
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=10
    )

    messages = response.get('Messages', [])
    if messages:
        for message in messages:
            number = message['Body']
            print(f"Received: {number}")

            # Save to file
            with open('numbers.txt', 'a') as f:
                f.write(f"{number}\n")

            # Delete the message from queue
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=message['ReceiptHandle']
            )
