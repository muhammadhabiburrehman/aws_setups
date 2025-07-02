# SQS Counter Project

## Overview

This project consists of two Python scripts that work together to demonstrate AWS SQS (Simple Queue Service) messaging:

- **Code1**: A producer script that sends incrementing numbers to an SQS queue every minute
- **Code2**: A consumer script that reads numbers from the SQS queue and stores them in a file

## Architecture

```
Code1 (Producer) → SQS Queue → Code2 (Consumer) → File Storage
```

## Files

- `code1.py` - Producer script that sends incrementing numbers to SQS
- `code2.py` - Consumer script that reads from SQS and writes to file
- `requirements.txt` - Python dependencies
- `numbers.txt` - Output file where numbers are stored

## Prerequisites

### AWS Setup
1. AWS account with SQS access
2. AWS credentials configured (one of the following):
   - AWS CLI configured (`aws configure`)
   - Environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)
   - IAM role (if running on EC2)

### Python Requirements
- Python 3.7+
- boto3 library

## Installation

1. Clone or download the project files

2. Install required Python packages:
```bash
pip install -r requirements.txt
```

3. Create an SQS queue in your AWS account:
   - Go to AWS SQS console
   - Create a new queue (Standard or FIFO)
   - Note the queue URL

4. Update the queue URL in both scripts or configuration file

## Configuration

Make sure to update the following in your scripts:

```python
# Replace with your actual SQS queue URL
QUEUE_URL = 'https://sqs.region.amazonaws.com/account-id/queue-name'
```

## Usage

### Running Code1 (Producer)

The producer script sends incrementing numbers to SQS every minute:

```bash
python code1.py
```

**What it does:**
- Starts with number 1
- Sends the current number to SQS queue
- Increments the counter
- Waits 1 minute
- Repeats the process

### Running Code2 (Consumer)

The consumer script reads messages from SQS and stores them in a file:

```bash
python code2.py
```

**What it does:**
- Polls the SQS queue for messages
- Reads the number from each message
- Appends the number to `numbers.txt`
- Deletes the processed message from the queue
- Continues polling

## Running Both Scripts

For the complete workflow, run both scripts simultaneously:

```bash
# Terminal 1
python code1.py

# Terminal 2 (in a separate terminal)
python code2.py
```

## Expected Behavior

1. **Code1** will output:
   ```
   Sent: 1
   Sent: 2
   Sent: 3   ...
   ```

2. **Code2** will output:
   ```
   Received: 1
   Received: 2
   Received: 3
   ...
   ```

3. **numbers.txt** will contain:
   ```
   1
   2
   3
   ...
   ```

## Error Handling

The scripts include error handling for:
- AWS connection issues
- SQS queue access problems
- File I/O errors
- Message processing failures

## Stopping the Scripts

- Use `Ctrl+C` to stop either script
- Code1 will stop sending new messages
- Code2 will process any remaining messages in the queue before stopping

## Troubleshooting

### Common Issues

1. **AWS Credentials Error**
   - Ensure AWS credentials are properly configured
   - Check IAM permissions for SQS access

2. **Queue Not Found**
   - Verify the queue URL is correct
   - Ensure the queue exists in the specified AWS region

3. **Permission Denied**
   - Check IAM policies allow SQS operations
   - Ensure the queue policy allows your AWS account access

4. **File Permission Error**
   - Check write permissions in the current directory
   - Ensure the output file is not locked by another process


## Customization

### Changing the Interval
Modify the sleep time in Code1:
```python
time.sleep(60)  # Change 60 to desired seconds
```

### Changing Output Format
Modify the file writing logic in Code2:
```python
# Add timestamp
 with open('numbers.txt', 'a') as f:
      f.write(f"{number}\n")
```

### Adding Queue Attributes
Configure message retention, visibility timeout, etc. in AWS SQS console or via boto3.

## Security Considerations

- Use IAM roles with minimal required permissions
- Consider using SQS dead letter queues for error handling
- Don't hardcode AWS credentials in your code
- Use environment variables or AWS parameter store for sensitive configuration