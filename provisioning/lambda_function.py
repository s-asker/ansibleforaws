import json
import urllib.parse
import requests

def lambda_handler(event, context):
    # Replace these placeholders with Ansible variables during deployment
    jenkins_base_url = "{{ jenkins_base_url }}"  # Base URL for Jenkins
    token = "{{ jenkins_token }}"               # Authentication token for Jenkins

    try:
        # Log the incoming SNS event
        print(f"Received event: {json.dumps(event)}")

        # URL encode the SNS message to safely include it in the query string
        encoded_message = urllib.parse.quote(sns_message)

        # Construct the Jenkins URL with query parameters
        jenkins_url = f"{jenkins_base_url}?token={token}"

        # Send the GET request to Jenkins webhook
        response = requests.get(jenkins_url)

        # Log the response from Jenkins
        print(f"Response from Jenkins: {response.status_code} - {response.text}")

        return {
            'statusCode': response.status_code,
            'body': response.text
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': str(e)
        }
