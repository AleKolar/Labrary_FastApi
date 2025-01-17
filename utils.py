import json

def json_to_dict(json_str):
    return json.loads(json_str)

def dict_to_json(obj):
    return json.dumps(obj)

