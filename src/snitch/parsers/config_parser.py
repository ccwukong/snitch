import json
from json.decoder import JSONDecodeError


class ConfigParser:
    # It takes a json string as input during object instantiation
    def __init__(self, data):
        self.__postman_collection = {}
        self.__openapi = {}

        try:
            config = json.loads(data)
            if 'postmanCollection' in data:
                self.__postman_collection['collection_file_path'] = config['postmanCollection']['collectionFilePath']
                self.__postman_collection['metadata'] = config['postmanCollection']['metadata']

            if 'openApi' in data:
                self.__openapi['file_path'] = config['openApi']['filePath']
                self.__openapi['metadata'] = config['openApi']['metadata']

            # TODO: add open api handler
        except JSONDecodeError as e:
            raise e

    @property
    def has_postman_collection(self):
        return True if self.__postman_collection else False

    @property
    def collection_metadata(self):
        return self.__postman_collection.get('metadata', None)

    @property
    def collection_file_path(self):
        return self.__postman_collection.get('collection_file_path', None)

    @property
    def has_openapi(self):
        return True if self.__openapi else False

    @property
    def openapi_metadata(self):
        return self.__openapi.get('metadata', None)

    @property
    def openapi_file_path(self):
        return self.__openapi.get('file_path', None)
