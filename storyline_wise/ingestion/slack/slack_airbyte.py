import airbyte as ab

source = ab.get_source(
    "source-slack",
    config={
        "api_token": "xoxb-whatever",
        "start_date": "2024-10-01T00:00:00Z",
        "lookback_window": 1,
        "join_channels": True,  # Will auto-join all channels the bot has access to
        # "channel_filter": ["test-slack-ingestion"],
    },
    install_if_missing=True,
)
source.check()
source.select_streams(
    [
        "channels",
        "channel_members",
        "channel_messages",
        # "threads",
    ]
)


result = source.read(force_full_refresh=True)

for name, records in result.streams.items():
    print(f"Stream {name}: {len(list(records))} records")
    for record in records:
        print(record)

print("done!")
