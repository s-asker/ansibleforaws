# lambda_function.py
import boto3
import os
import time

ec2 = boto3.client('ec2')
ssm = boto3.client('ssm')

def lambda_handler(event, context):
    instance_id = event['detail']['EC2InstanceId']
    bucket_name = os.environ['S3_BUCKET_NAME']  # Get bucket name from environment variable
    print(f"Scaling event detected: Instance {instance_id}")

    # Wait for the instance to initialize (optional)
    time.sleep(30)

    # Sync files from S3 to the instance using SSM
    command = f"aws s3 sync s3://{bucket_name} /var/www/html"

    ssm.send_command(
        InstanceIds=[instance_id],
        DocumentName="AWS-RunShellScript",
        Parameters={"commands": [command]},
    )
    print(f"Sync initiated for instance {instance_id} from bucket {bucket_name}.")
