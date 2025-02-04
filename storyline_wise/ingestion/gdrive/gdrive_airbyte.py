import json

import airbyte as ab

folder_url = "https://drive.google.com/drive/folders/..."

credentials = json.load(open("../gdrive_credentials.json"))

source = ab.get_source(
    "source-google-drive",
    config={
        "streams": [
            {
                "name": "everything",
                "format": {"filetype": "unstructured"},
            }
        ],
        "folder_url": folder_url,
        "credentials": {
            "auth_type": "Service",
            "service_account_info": json.dumps(credentials),
        },
    },
    install_if_missing=True,
)
source.check()
source.select_all_streams()


result = source.read(force_full_refresh=True)
for stream in result.streams:
    print(f"Stream {stream}: {len(list(result.streams[stream]))} records")
    for record in result.streams[stream]:
        print(record)
print("yay!")
