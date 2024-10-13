#!/bin/bash

# Get the token
TOKEN=$(curl -X PUT -H "X-aws-ec2-metadata-token-ttl-seconds: 300" http://169.254.169.254/latest/api/token)

# Get the instance ID using the token
INSTANCE_ID=$(curl http://169.254.169.254/latest/meta-data/instance-id -H "X-aws-ec2-metadata-token: $TOKEN")

# Get the region using the token
REGION=$(curl http://169.254.169.254/latest/meta-data/placement/availability-zone -H "X-aws-ec2-metadata-token: $TOKEN" | sed 's/[a-z]$//')

# Fetch instance details using AWS CLI
VPC_ID=$(aws ec2 describe-instances --instance-ids $INSTANCE_ID --region $REGION --query "Reservations[0].Instances[0].VpcId" --output text)

# Output the VPC ID
echo "VPC ID: $VPC_ID"