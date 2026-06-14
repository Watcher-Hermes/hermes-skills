# Publisher
def publish_event(channel: str, payload: dict):
    r.publish(channel, json.dumps(payload))