import os
from atlassian import Confluence
from dotenv import load_dotenv


load_dotenv("../../../.env")
# Initialize confluence with basic authentication
# replace username and password with your own


confluence = Confluence(
    url=f"https://{os.getenv('ATLASSIAN_DOMAIN_NAME')}/wiki",
    username=os.getenv("ATLASSIAN_USER"),
    password=os.getenv("ATLASSIAN_KEY"),
)


# we will index the HR space as an example
space = "my_space"

# Below we set limit=500 to retrieve all the pages at once
# However you can write a for loop to batch load the pages if
# there is a ton of them
pages = confluence.get_all_pages_from_space(
    space, start=0, limit=10, expand="body.storage", content_type="page"
)


# Each item in `pages` is a dictionary that holds lists, nested dictionaries,
# strings, etc. as metadata for that page (including id, title, etc.)
# The main html content of the page is retrieved via this nested dictionary:
print(pages[0]["body"]["storage"]["value"])
print("yay!")
