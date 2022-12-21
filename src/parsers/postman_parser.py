from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Union, List
from json.decoder import JSONDecodeError
from .config_parser import ConfigParser


class PostmanFileParser():
    def __init__(self, path, metadata={}):
        self.__requests = []
        try:
            with open(path, 'r') as f:
                data = json.loads(f.read())
                for i in data['item']:
                    headers = []
                    for h in i['request']['header']:
                        if h['value'] in metadata:
                            h['value'] = metadata[h['value']]
                        headers.append(PostmanRequestHeaderItem(
                            h['key'], h['value']))

                    for h in i['request']['url']['host']:
                        if h in metadata:
                            i['request']['url']['raw'] = i['request']['url']['raw'].replace(
                                h, metadata[h])

                    req = PostmanRequest(
                        i['name'], i['request']['url']['raw'], i['request']['method'], headers)

                    self.__requests.append(req)
        except JSONDecodeError as e:
            raise e  # TODO: handle this differently
        except FileNotFoundError as e:
            raise e

    @property
    def requests(self):
        return self.__requests


@dataclass
class PostmanRequest:
    method: str
    url: str
    headers: List[PostmanRequestHeaderItem]
    name: str = ''


@dataclass
class PostmanRequestHeaderItem:
    key: str
    value: Union[str, int, float]
