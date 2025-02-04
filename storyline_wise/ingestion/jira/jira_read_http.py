import os

from dotenv import load_dotenv
import requests


load_dotenv("../../../../.env")

BASE_URL = "https://{os.getenv('ATLASSIAN_DOMAIN_NAME')}"
USERNAME = os.getenv("ATLASSIAN_USER")
JIRA_API_TOKEN = os.getenv("ATLASSIAN_KEY")

# Example: Get issues from a project
url = f"{BASE_URL}/rest/api/3/search"

headers = {
    "Authorization": f"Basic {USERNAME}:{JIRA_API_TOKEN}",
    "Content-Type": "application/json",
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("Jira data retrieved successfully!")
    print(response.json())
else:
    print(f"Failed to retrieve Jira data. Status code: {response.status_code}")
