from __future__ import annotations

from dataclasses import dataclass
from typing import Union


@dataclass
class Request:
    method: str
    url: str
    headers: dict
    body: dict = None
    name: str = ''


@dataclass
class RequestHeader:
    key: str
    value: Union[str, int, float]
