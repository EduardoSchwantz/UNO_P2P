import json
from datetime import datetime

def make_message(msg_type, sender, payload=None):
    return json.dumps({
        "type": msg_type,
        "sender": sender,
        "timestamp": datetime.utcnow().isoformat(),
        "payload": payload or {}
    })

def parse_message(raw_data):
    return json.loads(raw_data)
