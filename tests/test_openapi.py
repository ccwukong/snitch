from src.snitch.parsers.openapi_parser import OpenApiParser
from src.snitch.parsers.request_model import Request
import unittest
from unittest.mock import patch, mock_open


class TestPostmanCollectionParser(unittest.TestCase):
    def setUp(self):
        self.data = '''openapi: 3.0.0
info:
  title: FarmWeather
  version: 1.0.0
servers:
  - url: '{{apiDomain}}'
paths:
  /users:
    get:
      tags:
        - default
      summary: Test API
      parameters:
        - name: Authorization
          in: header
          schema:
            type: string
          example: '{{accessToken}}'
        - name: x-api-key
          in: header
          schema:
            type: string
          example: '{{apiKey}}'
        - name: uid
          in: query
          schema:
            type: integer
          example: '123'
      responses:
        '200':
          description: Successful response
          content:
            application/json: {}'''

    def test_PostmanCollectionParser(self):
        with patch("builtins.open", mock_open(read_data=self.data)) as mock_file:
            reqs = OpenApiParser('')

        self.assertEqual(len(reqs.requests), 1)
        self.assertEqual(type(reqs.requests[0]), Request)
        self.assertEqual(reqs.requests[0].url, '{{apiDomain}}/users?uid=123')
