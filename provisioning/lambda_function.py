# lambda_function.py
import boto3
import time

ec2 = boto3.client('ec2')
ssm = boto3.client('ssm')

def lambda_handler(event, context):
    instance_id = event['detail']['EC2InstanceId']
    print(f"Scaling event detected: Instance {instance_id}")

    # Wait for the instance to initialize (optional)
    time.sleep(30)

    # Sync files from S3 to the instance using SSM
    command = "aws s3 sync s3://your-bucket-name /var/www/html"

    ssm.send_command(
        InstanceIds=[instance_id],
        DocumentName="AWS-RunShellScript",
        Parameters={"commands": [command]},
    )
    print(f"Sync initiated for instance {instance_id}.")
