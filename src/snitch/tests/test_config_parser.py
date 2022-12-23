from parsers.config_parser import ConfigParser
import unittest
import sys
import os
current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_path + '/../')


class TestConfigParser(unittest.TestCase):
    def setUp(self):
        self.__data = '''{
            "postmanCollection": {
                "version": "2.1",
                "collectionFilePath": "absolute_path_to_the_postman_collection_json_file",
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
                "filePath": "absolute_path_to_the_postman_collection_yaml_file",
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

    def test_config_parser(self):
        config = ConfigParser(self.__data)

        self.assertTrue(config.has_postman_collection)
        self.assertTrue(config.has_openapi)
