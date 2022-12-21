from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Union
from json.decoder import JSONDecodeError
from .config_parser import ConfigParser


class PostmanFileParser():
    def __init__(self, path):
        try:
            with open(path, 'r') as f:
                data = json.loads(f.read())
                self.__endpoints = data['item']
        except JSONDecodeError as e:
            raise e
        except FileNotFoundError as e:
            raise e
        # try:
        #     j = json.loads(data)
        #     print(j)
        #     return j
        # except JSONDecodeError as e:
        #     raise e

    @property
    def endpoints(self):
        return self.__endpoints


@dataclass
class PostmanRequest:
    method: str
    url: str
    header: PostmanRequestHeaderItem
    name: str = ''


@dataclass
class PostmanRequestHeaderItem:
    key: str
    value: Union[str, int, float]
