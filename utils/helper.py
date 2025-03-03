import json


def print_json(data):
    # Convert Python dictionary to a JSON string with indentation
    json_string = json.dumps(data, indent=2)
    print(json_string)