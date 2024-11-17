import requests
import webbrowser
from flask import Flask, request, jsonify

app = Flask(__name__)

# GitHub API and Token
GITHUB_DISPATCH_URL = "https://api.github.com/repos/sheshanksaya/e-commerce/dispatches"
GITHUB_TOKEN = "" #Replace github token

@app.route("/jira-webhook", methods=["POST"])
def jira_webhook():
    data = request.json
    if data.get("issue_event_type_name") == "issue_created":
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json",
        }
        payload = {
            "event_type": "jira_issue_created",
            "client_payload": {"issue_key": data["issue"]["key"]},
        }
        response = requests.post(GITHUB_DISPATCH_URL, json=payload, headers=headers)

        # Check if the response body is empty
        if response.status_code == 204:
            url = "https://sheshanksaya.github.io/e-commerce/index.html"  # Hardcoded URL of your HTML page
            webbrowser.open(url, new=2)  # Open the page in a new browser tab
            return {"message": "GitHub Action triggered successfully"}, 204
        else:
            try:
                return response.json(), response.status_code
            except ValueError:
                return {"error": "Unexpected response from GitHub API"}, response.status_code
    return {"message": "No action taken"}, 200


@app.route("/form-created", methods=["POST"])
def form_created():
    data = request.json
    if data.get("form_name"):
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json",
        }
        payload = {
            "event_type": "form_created",
            "client_payload": {"form_name": data["form_name"], "form_id": data.get("form_id")},
        }
        response = requests.post(GITHUB_DISPATCH_URL, json=payload, headers=headers)

        if response.status_code == 204:
            return {"message": "GitHub Action triggered for form creation"}, 204
        else:
            try:
                return response.json(), response.status_code
            except ValueError:
                return {"error": "Unexpected response from GitHub API"}, response.status_code
    return {"message": "No form data provided"}, 400


if __name__ == "__main__":
    app.run(port=5000)