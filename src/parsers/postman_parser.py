import json
from json.decoder import JSONDecodeError


def postman_parse(data):
    try:
        j = json.loads(data)
        return j
    except JSONDecodeError as e:
        raise e
