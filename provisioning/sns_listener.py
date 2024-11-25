from flask import Flask, request
import subprocess
import json

app = Flask(__name__)

# Define the endpoint to listen for incoming SNS messages
@app.route('/call-jenkins', methods=['POST'])
def sns_listener():
    # Extract the SNS message from the request
    sns_message = request.json  # Get JSON from the body of the request

    if sns_message.get('Type') == 'SubscriptionConfirmation':
        # Extract the TopicArn and Token from the SNS message
        topic_arn = sns_message.get('TopicArn')
        token = sns_message.get('Token')

        # Send a request to confirm the subscription
        confirm_url = f"http://sns.us-east-2.amazonaws.com/?Action=ConfirmSubscription&TopicArn={topic_arn}&Token={token}"
        response = requests.get(confirm_url)

        # If the subscription is successfully confirmed
        if response.status_code == 200:
            return jsonify({"status": "Subscription Confirmed"}), 200
        else:
            return jsonify({"status": "Failed to Confirm Subscription"}), 400



    # Jenkins details from the message or predefined in your server
    jenkins_url = "http://127.0.0.1:8080/generic-webhook-trigger/invoke?token=12932"

    # Log the Jenkins URL (for debugging)
    print(f"Triggering Jenkins job: {jenkins_url}")

    # Trigger Jenkins job using curl
    curl_command = f"curl {jenkins_url}"

    # Execute the curl command
    result = subprocess.run(curl_command, shell=True, capture_output=True)

    # Check if the curl command was successful
    if result.returncode == 0:
        return json.dumps({"status": "success"}), 200
    else:
        return json.dumps({"status": "failed", "error": result.stderr.decode()}), 500

if __name__ == '__main__':
    # Run the Flask app on port 5000 or any other port
    app.run(host='0.0.0.0', port=5000)
