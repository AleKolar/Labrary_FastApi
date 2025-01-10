import json


def json_to_dict(json_str):
    return json.loads(json_str)

def object_to_json(obj):
    return json.dumps(obj)
