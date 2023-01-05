import yaml
import json
from json.decoder import JSONDecodeError
from typing import List, Dict
from .request_model import Request, RequestHeader


class OpenApiParser:
    def __init__(self, path, metadata: Dict = {}) -> None:
        self.__requests = []
        self.__metadata = metadata
        try:
            with open(path, 'r') as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
                servers = [i['url'] for i in data['servers']]

                for s in servers:
                    for k, v in data['paths'].items():
                        method = self.__extract_method(v)
                        headers = self.__extract_header_items(
                            v[method.lower()]['parameters'])
                        queries = []
                        for q in [itm for itm in v[method.lower()]['parameters'] if itm['in'] == 'query']:
                            if q['example'] in self.__metadata:
                                q['example'] = self.__metadata[q['example']]
                            queries.append(f"{q['name']}={q['example']}")

                        if method in set(['POST', 'PUT']):
                            headers['content-type'] = 'application/json'

                        body = None

                        if 'requestBody' in v[method.lower()]:
                            if 'application/json' in v[method.lower()]['requestBody']['content']:
                                body = v[method.lower(
                                )]['requestBody']['content']['application/json']['schema']['example']
                            elif '*/*' in v[method.lower()]['requestBody']['content']:
                                body = v[method.lower(
                                )]['requestBody']['content']['*/*']['schema']['example']
                        while type(body) == str:
                            body = json.loads(body)

                        for key, val in self.__metadata.items():
                            s = s.replace(key, val)

                        req = Request(method, f"{s + k}{'?' + '&'.join(queries) if queries else ''}", headers,
                                      body, v[method.lower()]['summary'])

                        self.__requests.append(req)
        except JSONDecodeError as e:
            raise e  # TODO: handle this differently
        except FileNotFoundError as e:
            raise e

    def __extract_method(self, obj) -> str:
        if 'get' in obj:
            return 'GET'
        elif 'post' in obj:
            return 'POST'
        elif 'put' in obj:
            return 'PUT'
        elif 'delete' in obj:
            return 'DELETE'

    def __extract_header_items(self, arr) -> List[Dict[str, str]]:
        headers = {}
        for p in arr:
            if p['in'] == 'header':
                for k, v in self.__metadata.items():
                    p['example'] = p['example'].replace(k, v)
                h = RequestHeader(p['name'].lower(), p['example'])
                headers[h.key] = h.value

        return headers

    @property
    def requests(self):
        return self.__requests
