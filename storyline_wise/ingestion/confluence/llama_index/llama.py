import os
from llama_index.readers.confluence import ConfluenceReader

# pip install llama-index-readers-confluence
# https://llamahub.ai/l/readers/llama-index-readers-confluence?from=all

# from dotenv import load_dotenv
# env_path = os.path.realpath(os.path.join(os.path.dirname(__file__), "../../../../.env"))
# print("env_path:", env_path)
# success = load_dotenv(env_path)
# assert success, "Failed to load .env file"


def get_pages_for_space(
    space_key: str,
    base_url: str = None,
):
    base_url = base_url or f"https://{os.getenv('ATLASSIAN_DOMAIN_NAME')}/wiki"
    os.environ["CONFLUENCE_USERNAME"] = os.getenv("ATLASSIAN_USER")
    os.environ["CONFLUENCE_PASSWORD"] = os.getenv("ATLASSIAN_KEY")
    reader = ConfluenceReader(base_url=base_url)
    documents = reader.load_data(space_key=space_key, include_attachments=False)
    return documents
