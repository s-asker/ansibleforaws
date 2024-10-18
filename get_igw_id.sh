#!/bin/bash

# Check if both VPC ID and region are provided
region="us-east-2"
vpc_id=$1

# Get the Internet Gateway ID
igw_id=$(aws ec2 describe-internet-gateways \
  --region "$region" \
  --filters Name=attachment.vpc-id,Values="$vpc_id" \
  --query 'InternetGateways[0].InternetGatewayId' \
  --output text)

# Check if IGW ID is empty or None
if [[ -z "$igw_id" || "$igw_id" == "None" ]]; then
  echo "No IGW found"
  exit 1
else
  echo "$igw_id"
fi
