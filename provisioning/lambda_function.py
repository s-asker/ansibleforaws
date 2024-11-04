import boto3
import time
import os

ec2 = boto3.client('ec2')
ssm = boto3.client('ssm')

def lambda_handler(event, context):
    # Extract the instance ID from the event using the correct key
    instance_id = event['detail']['instance-id']  # Updated to match the event structure
    print(f"Scaling event detected: Instance {instance_id}")

    # Optionally wait for the instance to initialize
    time.sleep(30)  # Adjust this value as needed

    # Prepare the S3 bucket name from an environment variable or hard-code it
    bucket_name = os.environ.get('S3_BUCKET_NAME', 'your-bucket-name')  # Set your bucket name here or through environment variables

    # Command to sync files from S3 to the instance using SSM
    command = f"aws s3 sync s3://{bucket_name} /var/www/html"

    try:
        # Send command to the instance via SSM
        response = ssm.send_command(
            InstanceIds=[instance_id],
            DocumentName="AWS-RunShellScript",
            Parameters={"commands": [command]},
        )
        command_id = response['Command']['CommandId']
        print(f"Sync initiated for instance {instance_id}. Command ID: {command_id}")

        # Optionally wait for the command to complete (can be improved)
        time.sleep(10)  # Adjust based on command execution time

        # Check the command's output
        command_response = ssm.list_commands(CommandId=command_id)
        print(f"Command response: {command_response}")

    except Exception as e:
        print(f"Error sending command to instance {instance_id}: {str(e)}")
