#!/bin/bash

# Get the token
TOKEN=$(curl -X PUT -H "X-aws-ec2-metadata-token-ttl-seconds: 300" http://169.254.169.254/latest/api/token)

# Get the instance ID using the token
INSTANCE_ID=$(curl http://169.254.169.254/latest/meta-data/instance-id -H "X-aws-ec2-metadata-token: $TOKEN")

# Output the instance ID
echo $INSTANCE_ID
