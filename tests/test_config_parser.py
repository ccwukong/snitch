from snitch.parsers.config_parser import ConfigParser
from snitch.parsers.parser_exceptions import InvalidPostmanCollectionVersion, InvalidOpenApiVersion
import unittest
import json


class TestConfigParser(unittest.TestCase):
    def setUp(self):
        self.__data = '''{
            "postmanCollection": {
                "version": "2.1",
                "filePath": "absolute_path_to_the_postman_collection_json_file",
                "metadata": {
                    "{{restUrl}}": "https://your_api_domain",
                    "{{accessToken}}": "the access token string",
                    "{{apiKey}}": "api key string"
                },
                "header": {
                    "Authorization": "{{accessToken}}",
                    "x-api-key": "{{apiKey}}"
                }
            },
            "openApi": {
                "version": "3.0.0",
                "filePath": "absolute_path_to_the_open_api_yaml_file",
                "metadata": {
                    "{{restUrl}}": "https://your_api_domain",
                    "{{accessToken}}": "the access token string",
                    "{{apiKey}}": "api key string"
                },
                "header": {
                    "Authorization": "{{accessToken}}",
                    "x-api-key": "{{apiKey}}"
                }
            }
        }'''

    def test_ConfigParser(self):
        config = ConfigParser(self.__data)

        self.assertTrue(config.has_postman_collection)
        self.assertTrue(config.has_openapi)
        self.assertEqual(config.collection_metadata, {
            "{{restUrl}}": "https://your_api_domain",
            "{{accessToken}}": "the access token string",
            "{{apiKey}}": "api key string"
        })
        self.assertEqual(config.openapi_metadata, {
            "{{restUrl}}": "https://your_api_domain",
            "{{accessToken}}": "the access token string",
            "{{apiKey}}": "api key string"
        })
        self.assertEqual(config.collection_file_path,
                         "absolute_path_to_the_postman_collection_json_file")
        self.assertEqual(config.openapi_file_path,
                         "absolute_path_to_the_open_api_yaml_file")

    def test_ConfigParser_InvalidPostmanCollectionVersion(self):
        tmp = json.loads(self.__data)
        tmp['postmanCollection']['version'] = '1.0'
        tmp['openApi']['version'] = '3.0.0'
        self.__data = json.dumps(tmp)

        with self.assertRaises(InvalidPostmanCollectionVersion):
            ConfigParser(self.__data)

    def test_ConfigParser_InvalidOpenApiVersion(self):
        tmp = json.loads(self.__data)
        tmp['postmanCollection']['version'] = '2.1'
        tmp['openApi']['version'] = '2.0.0'
        self.__data = json.dumps(tmp)

        with self.assertRaises(InvalidOpenApiVersion):
            ConfigParser(self.__data)
