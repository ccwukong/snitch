from __future__ import annotations

import yaml


class OpenApiParser:
    def __init__(self, path, metadata={}):
        try:
            with open(path, 'r') as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
                print(data)
        except Exception as e:
            raise e
