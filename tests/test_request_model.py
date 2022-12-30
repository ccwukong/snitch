from snitch.parsers.request_model import Request, RequestHeader
import unittest


class TestRequestModel(unittest.TestCase):
    def test_Request(self):
        r = Request('POST', 'https://example.com',
                    {'authorization': 'token', 'x-api-key': 'key'}, None, 'test api')

        self.assertEqual(r.name, 'test api')
        self.assertEqual(r.url, 'https://example.com')
        self.assertEqual(r.method, 'POST')
        self.assertEqual(r.body, None)
        self.assertEqual(
            r.headers, {'authorization': 'token', 'x-api-key': 'key'})

    def test_RequestHeader(self):
        r = RequestHeader('content-type', 'application/json')

        self.assertEqual(r.key, 'content-type')
        self.assertEqual(r.value, 'application/json')
