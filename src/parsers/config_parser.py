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
                # if access token exists is configured
                if 'accessToken' in config['postmanCollection']['auth'] and \
                        config['postmanCollection']['auth']['accessToken']:
                    self.__postman_collection['access_token'] = config['postmanCollection']['auth']['accessToken']

                # if user credentials exists is configured
                if 'userCredential' in config['postmanCollection']['auth'] and \
                        config['postmanCollection']['auth']['userCredential']:
                    self.__postman_collection['user'] = config['postmanCollection']['auth']['userCredential']['user']
                    self.__postman_collection['password'] = config['postmanCollection']['auth']['userCredential']['password']

                self.__postman_collection['collection_file_path'] = config['postmanCollection']['collectionFilePath']
                self.__postman_collection['restApiUrl'] = config['postmanCollection']['restApiUrlPrefix']
                self.__postman_collection['header'] = config['postmanCollection']['header']

            # TODO: add open api handler
        except JSONDecodeError as e:
            raise e

    @property
    def has_postman_collection(self):
        return True if self.__postman_collection else False

    @property
    def access_token(self):
        return self.__postman_collection.get('access_token', None)

    @property
    def reqeust_header(self):
        return self.__postman_collection.get('header', None)

    @property
    def rest_api_url(self):
        return self.__postman_collection.get('restApiUrl', None)

    @property
    def collection_file_path(self):
        return self.__postman_collection.get('collection_file_path', None)
