import os

from atlassian import Confluence
from dotenv import load_dotenv


load_dotenv("../../../.env")

confluence = Confluence(
    url=f"https://{os.getenv('ATLASSIAN_DOMAIN_NAME')}/wiki",
    username=os.getenv("ATLASSIAN_USER"),
    password=os.getenv("ATLASSIAN_KEY"),
)

# Page details
PAGE_ID = "..."  # ID of the page you want to modify

# Get the existing page data
page_data = confluence.get_page_by_id(page_id=PAGE_ID, expand="body.storage,version")

# Extract necessary data for updating the page
current_version = page_data["version"]["number"]
current_title = page_data["title"]
new_content = "<h1>Updated Content</h1><p>This is the updated content of the page.</p>"

# Update the page with new content
response = confluence.update_page(
    page_id=PAGE_ID,
    title=current_title,  # Keep the title the same, or you can change it
    body=new_content,  # Increment the version
)

if response:
    print("Page updated successfully!")
else:
    print("Failed to update the page.")

print("works!")
