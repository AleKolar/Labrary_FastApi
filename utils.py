import json

from sqlalchemy.orm import InstanceState


# def json_to_dict(json_str):
#     if isinstance(json_str, str):
#         return json.loads(json_str)
#     else:
#         raise ValueError("Input must be a string")
#
# def object_to_json(obj):
#     if isinstance(obj, dict):
#         return json.dumps(obj)
#     if isinstance(obj, InstanceState):
#         return json.dumps(obj._asdict())
#     return json.dumps(obj.__dict__)

def json_to_dict(json_str):
    return json.loads(json_str)

def object_to_json(obj):
    return json.dumps(obj)
