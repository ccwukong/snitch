import yaml
from json.decoder import JSONDecodeError
from .request_model import Request, RequestHeader


class OpenApiParser:
    def __init__(self, path, metadata={}):
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

                        if method in set(['POST', 'PUT']):
                            headers.append(
                                {'content-type': 'application/json'})

                        body = {}

                        if 'requestBody' in v[method.lower()]:
                            if 'application/json' in v[method.lower()]['requestBody']['content']:
                                body = v[method.lower(
                                )]['requestBody']['content']['application/json']['schema']['example']
                            elif '*/*' in v[method.lower()]['requestBody']['content']:
                                body = v[method.lower(
                                )]['requestBody']['content']['*/*']['schema']['example']

                        req = Request(method, s + k, headers,
                                      body, v[method.lower()]['summary'])

                        self.__requests.append(req)

        except FileNotFoundError as e:
            raise e
        except Exception as e:
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

    def __extract_header_items(self, arr) -> list[dict[str, str]]:
        headers = []
        for p in arr:
            if p['in'] == 'header':
                if p['example'] in self.__metadata:
                    p['example'] = self.__metadata[p['example']]
                h = RequestHeader(p['name'], p['example'])
                headers.append({h.key: h.value})

        return headers

    @property
    def requests(self):
        return self.__requests
