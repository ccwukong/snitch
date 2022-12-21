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

            # TODO: add open api handler
        except JSONDecodeError as e:
            raise e

    @property
    def has_postman_collection(self):
        return True if self.__postman_collection else False

    @property
    def metadata(self):
        return self.__postman_collection.get('metadata', None)

    @property
    def collection_file_path(self):
        return self.__postman_collection.get('collection_file_path', None)
