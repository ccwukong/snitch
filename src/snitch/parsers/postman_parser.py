import json
from json.decoder import JSONDecodeError
from .request_model import Request, RequestHeader


class PostmanFileParser():
    def __init__(self, path, metadata={}):
        self.__requests = []
        try:
            with open(path, 'r') as f:
                data = json.loads(f.read())
                for i in data['item']:
                    # transform the header entries from list to dict
                    headers = {}
                    for h in i['request']['header']:
                        if h['value'] in metadata:
                            h['value'] = metadata[h['value']]
                        hi = RequestHeader(
                            h['key'].lower(), h['value'])
                        headers[hi.key] = hi.value

                    # edge case, if method is POST but content-type is missing
                    if i['request']['method'] == 'POST':
                        headers['content-type'] = 'application/json'

                    # replacing the placeholders in url
                    for h in i['request']['url']['host']:
                        if h in metadata:
                            i['request']['url']['raw'] = i['request']['url']['raw'].replace(
                                h, metadata[h])

                    # body payload could be malformatted
                    # TODO: support content-type other than application/json
                    body = None
                    try:
                        if 'body' in i['request'] and i['request']['body']['mode'] == 'raw':
                            body = json.loads(
                                i['request']['body']['raw'].strip())
                    except Exception as e:
                        body = None

                    req = Request(
                        i['request']['method'], i['request']['url']['raw'], headers, body, i['name'])

                    self.__requests.append(req)
        except JSONDecodeError as e:
            raise e  # TODO: handle this differently
        except FileNotFoundError as e:
            raise e

    @property
    def requests(self):
        return self.__requests
