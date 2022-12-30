from snitch.task_runners.idempotency_check import run_idempotency_check
from snitch.parsers.request_model import Request
from snitch.logger import LogItem
import unittest
from unittest.mock import patch, Mock, MagicMock


class TestIdempotencyCheck(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.data = [Request('GET', 'https://example.com',
                             {'content-type', 'application/json'}, None, 'Test API')]
        self.request = Mock()
        self.request.url = 'https://example.com'
        self.request.headers = {'content-type': 'application/json'}
        self.request.body = None
        self.request.method = 'GET'
        self.request.name = 'Test API'

        self.response = Mock()
        self.response.status_code = 201
        self.response.text = 'content'

    async def test_run_idempotency_check_get(self):
        with patch("requests.get") as request_mock:
            request_mock.return_value = self.response
            res = await run_idempotency_check(self.request)

        self.assertEqual(res['error'], False)

    async def test_run_idempotency_check_post(self):
        with patch("requests.post") as async_mock:
            self.request.method = 'POST'
            async_mock.return_value = self.response

            res = await run_idempotency_check(self.request)

        self.assertEqual(res['error'], False)

    async def test_run_idempotency_check_put(self):
        with patch("requests.put") as async_mock:
            self.request.body = {}
            self.request.method = 'PUT'
            async_mock.return_value = self.response

            res = await run_idempotency_check(self.request)

        self.assertEqual(res['error'], False)

    async def test_run_idempotency_check_delete_error(self):
        with patch("requests.delete") as async_mock:
            self.request.body = None
            self.request.method = 'DELETE'
            self.response.status_code = 400
            async_mock.return_value = self.response
            res = await run_idempotency_check(self.request)

        self.assertEqual(res['error'], True)
