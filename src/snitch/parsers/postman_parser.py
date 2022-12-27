import json
from json.decoder import JSONDecodeError
from .request_model import Request, RequestHeader


class PostmanCollectionParser():
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
                    if i['request']['method'] in set(['POST', 'PUT']):
                        headers['content-type'] = 'application/json'

                    # replacing the placeholders in url
                    if type(i['request']['url']) == str:
                        url_str = i['request']['url']
                        for h in metadata:
                            url_str = url_str.replace(h, metadata[h])
                    else:
                        url_str = i['request']['url']['raw']

                        for h in i['request']['url']['host']:
                            if h in metadata:
                                url_str = url_str.replace(h, metadata[h])

                    # body payload could be malformatted
                    # TODO: support content-type other than application/json
                    body = None
                    try:
                        if 'body' in i['request'] and i['request']['body']['mode'] == 'raw':
                            body = json.loads(
                                i['request']['body']['raw'].strip())

                            while type(body) == str:
                                body = json.loads(body)
                    except Exception as e:
                        body = None

                    req = Request(
                        i['request']['method'], url_str, headers, body, i['name'])

                    self.__requests.append(req)
        except JSONDecodeError as e:
            raise e  # TODO: handle this differently
        except FileNotFoundError as e:
            raise e

    @property
    def requests(self):
        return self.__requests
