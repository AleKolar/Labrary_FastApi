import json

from sqlalchemy.orm import InstanceState

# Var. 1
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

# Var. 2
# def json_to_dict(json_str):
#     return json.loads(json_str)
#
# def object_to_json(obj):
#     return json.dumps(obj)

def object_to_dict(obj):
    if hasattr(obj, "__dict__"):
        return obj.__dict__
    return obj

def dict_to_object(obj_dict, obj_class):
    return obj_class(**obj_dict)