from __future__ import annotations

from dataclasses import dataclass
from typing import Union, Dict


@dataclass
class Request:
    method: str
    url: str
    headers: Dict
    body: Dict = None
    name: str = ''


@dataclass
class RequestHeader:
    key: str
    value: Union[str, int, float]
