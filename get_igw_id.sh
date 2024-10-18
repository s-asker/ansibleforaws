#!/bin/bash

# Usage: ./get_igw_id.sh <vpc-id>
# Example: ./get_igw_id.sh vpc-12345678

# Check if VPC ID is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <vpc-id>"
  exit 1
fi

VPC_ID=$1

# Get the Internet Gateway ID associated with the VPC
IGW_ID=$(aws ec2 describe-internet-gateways \
  --filters "Name=attachment.vpc-id,Values=${VPC_ID}" \
  --query "InternetGateways[0].InternetGatewayId" \
  --output text)

# Check if the IGW was found
if [ "$IGW_ID" == "None" ]; then
  echo "No Internet Gateway found for VPC ID: $VPC_ID"
  exit 1
fi

# Print the Internet Gateway ID
echo "Internet Gateway ID for VPC $VPC_ID: $IGW_ID"
