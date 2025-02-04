import os

from atlassian import Confluence
from dotenv import load_dotenv

load_dotenv("../../../.env")
# Confluence instance URL and credentials
confluence = Confluence(
    url=f"https://{os.getenv('ATLASSIAN_DOMAIN_NAME')}/wiki",
    username=os.getenv("ATLASSIAN_USER"),
    password=os.getenv("ATLASSIAN_KEY"),
)

# Page details
PARENT_PAGE_ID = "..."  # ID of the parent page
SPACE_KEY = "..."

# New page details
new_page_title = "New Child Page"
new_page_content = (
    "<h1>This is the new child page</h1><p>Content for the new child page.</p>"
)

# Create the new page under the specified parent page
response = confluence.create_page(
    space=SPACE_KEY,
    title=new_page_title,
    body=new_page_content,
    parent_id=PARENT_PAGE_ID,
)

if response:
    print(f"Page created successfully! Page ID: {response['id']}")
else:
    print("Failed to create the page.")

print("yay!")
