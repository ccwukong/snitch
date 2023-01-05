import json
from json.decoder import JSONDecodeError
from typing import List, Dict
from .request_model import Request, RequestHeader


class PostmanCollectionParser():
    def __init__(self, path, metadata={}) -> None:
        self.__requests = []
        try:
            with open(path, 'r') as f:
                data = json.loads(f.read())
                items = self.__flatten_paths(data['item'])
                for i in items:
                    # transform the header entries from list to dict
                    headers = {}

                    # edge case, item field in item
                    for h in i['request']['header']:
                        for k, v in metadata.items():
                            h['value'] = h['value'].replace(k, v)

                        hi = RequestHeader(
                            h['key'].lower(), h['value'])
                        headers[hi.key] = hi.value

                    # edge case, if method is POST but content-type is missing
                    if i['request']['method'] in set(['POST', 'PUT']):
                        headers['content-type'] = 'application/json'

                    # replacing the placeholders in url
                    if type(i['request']['url']) == str:
                        url_str = i['request']['url']

                        if url_str:
                            for h in metadata:
                                url_str = url_str.replace(h, metadata[h])
                        else:
                            continue
                    else:
                        url_str = i['request']['url']['raw']

                        if url_str:
                            for h in i['request']['url']['host']:
                                if h in metadata:
                                    url_str = url_str.replace(h, metadata[h])
                        else:
                            continue

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

    def __flatten_paths(self, paths: List[Dict]) -> List[Dict]:
        items = []

        def dfs(item) -> None:
            if 'item' not in item:
                items.append(item)
                return

            for i in item['item']:
                dfs(i)

        for p in paths:
            dfs(p)

        return items

    @property
    def requests(self) -> List[Request]:
        return self.__requests
