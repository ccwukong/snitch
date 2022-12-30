import json
from typing import Union, Dict
from .parser_exceptions import InvalidOpenApiVersion, InvalidPostmanCollectionVersion
from ..typed import Number


class ConfigParser:
    # It takes a json string as input during object instantiation
    def __init__(self, data: str) -> None:
        self.__postman_collection = {}
        self.__openapi = {}

        try:
            config = json.loads(data)
            if 'postmanCollection' in config:
                if int(config['postmanCollection']['version'].split('.')[0]) < 2:
                    raise InvalidPostmanCollectionVersion(
                        'Error. snitch requires Postman collection version >= 2.0')
                self.__postman_collection['file_path'] = config['postmanCollection']['filePath']
                self.__postman_collection['metadata'] = config['postmanCollection']['metadata']

            if 'openApi' in config:
                if int(config['openApi']['version'].split('.')[0]) < 3:
                    raise InvalidOpenApiVersion(
                        'Error. snitch requires Open API version >= 3.0.0')
                self.__openapi['file_path'] = config['openApi']['filePath']
                self.__openapi['metadata'] = config['openApi']['metadata']
        except Exception as e:
            raise e

    @property
    def has_postman_collection(self) -> bool:
        return True if self.__postman_collection else False

    @property
    def collection_metadata(self) -> Union[Dict[str, Union[str, Number]], None]:
        return self.__postman_collection.get('metadata', None)

    @property
    def collection_file_path(self) -> Union[str, None]:
        return self.__postman_collection.get('file_path', None)

    @property
    def has_openapi(self) -> bool:
        return True if self.__openapi else False

    @property
    def openapi_metadata(self) -> Union[Dict[str, Union[str, Number]], None]:
        return self.__openapi.get('metadata', None)

    @property
    def openapi_file_path(self) -> Union[str, None]:
        return self.__openapi.get('file_path', None)
