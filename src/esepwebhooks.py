import json
import os
import requests


def lambda_handler(event, context):
    # Log the received event
    print(f"FunctionHandler received: {event}")

    # Get the body of the event
    body = event.get("body")
    if body:
        # Parse the JSON body to extract the issue URL
        try:
            data = json.loads(body)  # Convert JSON string to a Python dictionary
            issue_url = data.get("issue", {}).get("html_url")

            if issue_url:
                # Format the message payload
                payload = {
                    "text": f"Issue Created: {issue_url}"
                }

                # Get Slack webhook URL from environment variable
                slack_url = os.getenv("SLACK_URL")
                if not slack_url:
                    return {
                        'statusCode': 500,
                        'body': json.dumps("Error: SLACK_URL environment variable is not set.")
                    }

                # Send the POST request to Slack
                response = requests.post(slack_url, json=payload)

                # Check the response from Slack
                if response.status_code == 200:
                    return {
                        'statusCode': 200,
                        'body': json.dumps("Message sent to Slack successfully.")
                    }
                else:
                    return {
                        'statusCode': response.status_code,
                        'body': json.dumps(f"Failed to send message to Slack: {response.text}")
                    }
            else:
                return {
                    'statusCode': 400,
                    'body': json.dumps("Error: Issue URL not found in the payload.")
                }

        except json.JSONDecodeError:
            return {
                'statusCode': 400,
                'body': json.dumps("Error: Invalid JSON format.")
            }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps("Error: No body found in event.")
        }