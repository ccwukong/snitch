from snitch.parsers.postman_parser import PostmanCollectionParser
from snitch.parsers.request_model import Request
import unittest
from unittest.mock import patch, mock_open
from json.decoder import JSONDecodeError


class TestPostmanCollectionParser(unittest.TestCase):
    def setUp(self):
        self.data = '''{"info": {"_postman_id": "8d7c5957-b22d-40f1-a155-9116a1a92442","name": "test",
                            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
                            "_exporter_id": "6670289"}, "item": [{"name": "Test endpoint","request": {"method": "GET","header":
                            [{"key": "Authorization","type": "text","value": "Bearer {{accessToken}}"},{
                                "key": "x-api-key","type": "text","value": "{{apiKey}}"}],
                                    "url": {"raw": "{{apiDomain}}/users?uid=123","host": ["{{apiDomain}}"],"path": ["users"],"query":
                                    [{"key": "uid","value": "123"}]}},"response": []}]}'''

    def test_PostmanCollectionParser(self):
        with patch("builtins.open", mock_open(read_data=self.data)) as mock_file:
            reqs = PostmanCollectionParser('')

        self.assertEqual(len(reqs.requests), 1)
        self.assertEqual(type(reqs.requests[0]), Request)
        self.assertEqual(
            reqs.requests[0].headers['authorization'], 'Bearer {{accessToken}}')
        self.assertEqual(reqs.requests[0].url, '{{apiDomain}}/users?uid=123')

    def test_PostmanCollectionParser_error(self):
        with patch("builtins.open", mock_open(read_data=self.data+',')) as mock_file:
            with self.assertRaises(JSONDecodeError):
                reqs = PostmanCollectionParser('')
