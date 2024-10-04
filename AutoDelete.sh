#!/bin/bash

# Define the AWS region
region="us-east-2"  # Replace with your desired AWS region

# Find all VPCs with the tag Project: AnsibleCloudProject in the specified region
vpc_ids=$(aws ec2 describe-vpcs --region $region --filters "Name=tag:Project,Values=AnsibleCloudProject" --query "Vpcs[].VpcId" --output text)

# Loop through each VPC and delete its dependencies first
for vpc_id in $vpc_ids; do
  echo "Deleting dependencies for VPC with ID: $vpc_id in region $region"

  # Terminate all EC2 instances in the VPC
  instance_ids=$(aws ec2 describe-instances --region $region --filters "Name=vpc-id,Values=$vpc_id" --query "Reservations[].Instances[].InstanceId" --output text)
  if [ -n "$instance_ids" ]; then
    echo "Terminating EC2 instances: $instance_ids"
    aws ec2 terminate-instances --region $region --instance-ids $instance_ids
    # Wait for termination to complete
    aws ec2 wait instance-terminated --region $region --instance-ids $instance_ids
  fi

  # Delete all subnets in the VPC
  subnet_ids=$(aws ec2 describe-subnets --region $region --filters "Name=vpc-id,Values=$vpc_id" --query "Subnets[].SubnetId" --output text)
  if [ -n "$subnet_ids" ]; then
    echo "Deleting subnets: $subnet_ids"
    for subnet_id in $subnet_ids; do
      aws ec2 delete-subnet --region $region --subnet-id $subnet_id
    done
  fi

  # Detach and delete any Internet Gateways
  igw_ids=$(aws ec2 describe-internet-gateways --region $region --filters "Name=attachment.vpc-id,Values=$vpc_id" --query "InternetGateways[].InternetGatewayId" --output text)
  if [ -n "$igw_ids" ]; then
    for igw_id in $igw_ids; do
      echo "Detaching Internet Gateway: $igw_id"
      aws ec2 detach-internet-gateway --region $region --internet-gateway-id $igw_id --vpc-id $vpc_id
      echo "Deleting Internet Gateway: $igw_id"
      aws ec2 delete-internet-gateway --region $region --internet-gateway-id $igw_id
    done
  fi

  # Delete custom route tables in the VPC (the main route table cannot be deleted)
  route_table_ids=$(aws ec2 describe-route-tables --region $region --filters "Name=vpc-id,Values=$vpc_id" --query "RouteTables[?Associations[?Main==\`false\`]].RouteTableId" --output text)
  if [ -n "$route_table_ids" ]; then
    echo "Deleting route tables: $route_table_ids"
    for route_table_id in $route_table_ids; do
      aws ec2 delete-route-table --region $region --route-table-id $route_table_id
    done
  fi

  # Delete all security groups in the VPC (the default security group cannot be deleted)
  security_group_ids=$(aws ec2 describe-security-groups --region $region --filters "Name=vpc-id,Values=$vpc_id" --query "SecurityGroups[?GroupName!=\`default\`].GroupId" --output text)
  if [ -n "$security_group_ids" ]; then
    echo "Deleting security groups: $security_group_ids"
    for sg_id in $security_group_ids; do
      aws ec2 delete-security-group --region $region --group-id $sg_id
    done
  fi

  # Now, delete the VPC itself
  echo "Deleting VPC with ID: $vpc_id"
  aws ec2 delete-vpc --region $region --vpc-id $vpc_id
done

