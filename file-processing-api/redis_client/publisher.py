import json
from .client import r

def publish_message(channel: str, message: dict):
    r.publish(channel, json.dumps(message))