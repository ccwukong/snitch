import unittest
import sys
import os
current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_path + '/../')
from parsers.request_model import Request, RequestHeader

class TestRequestModel(unittest.TestCase):
    def test_request(self):
        r = Request('POST', 'https://example.com',
                    {'authorization': 'token', 'x-api-key': 'key'}, None, 'test api')

        self.assertEqual(r.name, 'test api')
