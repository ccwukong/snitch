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
                if 'apiKey' in config['postmanCollection']:
                    self.__postman_collection['api_key'] = config['postmanCollection']['apiKey']

                # if access token exists is configured
                if 'accessToken' in config['postmanCollection']['auth'] and \
                        config['postmanCollection']['auth']['accessToken']:
                    self.__postman_collection['access_token'] = config['postmanCollection']['auth']['accessToken']

                # if user credentials exists is configured
                if 'userCredential' in config['postmanCollection']['auth'] and \
                        config['postmanCollection']['auth']['userCredential']:
                    self.__postman_collection['user'] = config['postmanCollection']['auth']['userCredential']['user']
                    self.__postman_collection['password'] = config['postmanCollection']['auth']['userCredential']['password']

                self.__postman_collection['postman_collection_file_path'] = config['postmanCollection']['collectionFilePath']

            # TODO: add open api handler
        except JSONDecodeError as e:
            raise e

    @property
    def api_key(self):
        return self.__postman_collection.get('api_key', None)

    @property
    def access_token(self):
        return self.__postman_collection.get('access_token', None)

    @property
    def postman_collection_file_path(self):
        return self.__postman_collection.get('postman_collection_file_path', None)
