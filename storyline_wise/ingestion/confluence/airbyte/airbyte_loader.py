import os
from pathlib import Path

import airbyte as ab
from dotenv import load_dotenv


load_dotenv("../../../.env")

confluence_source = ab.get_source(
    "source-confluence",
    # source_manifest=Path("confluence_with_filter_by_space_keys.yaml"),
    config={
        "api_token": os.getenv("ATLASSIAN_KEY"),
        "domain_name": os.getenv("ATLASSIAN_DOMAIN_NAME"),
        "email": os.getenv("ATLASSIAN_USER"),
        # "space_keys": ["my_space_key"],
    },
    install_if_missing=True,
)

# Check connections
confluence_source.check()

# Select streams
confluence_source.select_streams(["pages", "blog_posts", "space"])

# Read data
confluence_result = confluence_source.read(force_full_refresh=True)

data = {}

for name, records in confluence_result.streams.items():
    print(f"Stream {name}: {len(list(records))} records")
    data[name] = list(records)

print("done!")
