import os

from atlassian import Jira
from dotenv import load_dotenv
import pandas as pd

load_dotenv("../../.env")


# Jira instance URL and credentials
JIRA_URL = f"https://{os.getenv('ATLASSIAN_DOMAIN_NAME')}"
USERNAME = os.getenv("ATLASSIAN_USER")
JIRA_API_TOKEN = os.getenv("ATLASSIAN_KEY")

# Initialize the Jira client
jira = Jira(url=JIRA_URL, username=USERNAME, password=JIRA_API_TOKEN)

# Example: Get all issues from a specific Jira project
project_key = "Something"  # Replace with your project key
issue_id = "..."
issues = jira.jql(f'project = "{project_key}" AND issue={issue_id}')

these_issues = {k: v for k, v in issues["issues"][0]["fields"].items() if v}
# Print the list of issues
if issues:
    print("Jira issues retrieved successfully!")
    for issue in issues["issues"]:
        print(f"Issue Key: {issue['key']}, Summary: {issue['fields']['summary']}")
else:
    print("No issues found, or failed to retrieve Jira issues.")

pd.DataFrame(issues["issues"])
