from snitch.task_runners.health_check import run_health_check, request
from snitch.parsers.request_model import Request
from snitch.logger import LogItem
import unittest
import aiohttp
from unittest.mock import patch, AsyncMock, Mock, MagicMock


class TestHealthCheck(unittest.IsolatedAsyncioTestCase):
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
        self.response.status = 201
        self.response.content = 'content'
        self.response.text = lambda: 'text'

    async def test_run_health_check_get(self):
        with patch("snitch.task_runners.health_check.get_all_requests", new_callable=AsyncMock) as async_mock:
            async_mock.return_value = [
                LogItem(False, 1, '', 'Test API')]
            res = await run_health_check(self.data)

            self.assertEqual(res['total'], 1)
            self.assertEqual(res['success'], 1)

    async def test_request_get(self):
        with patch("aiohttp.ClientSession.get", new_callable=AsyncMock) as async_mock:
            async_mock.return_value = self.response

            session = aiohttp.ClientSession
            session.get = MagicMock()
            session.get.return_value.__aenter__.return_value.status = 200
            session.get.return_value.__aenter__.return_value.text.return_value = 'test content'
            res = await request(session, self.request)

        self.assertEqual(res.has_err, False)
        self.assertEqual(res.name, 'Test API')

    async def test_request_post(self):
        with patch("aiohttp.ClientSession.post", new_callable=AsyncMock) as async_mock:
            self.request.method = 'POST'
            async_mock.return_value = self.response

            session = aiohttp.ClientSession
            session.post = MagicMock()
            session.post.return_value.__aenter__.return_value.status = 200
            session.post.return_value.__aenter__.return_value.text.return_value = 'test content'
            res = await request(session, self.request)

        self.assertEqual(res.has_err, False)
        self.assertEqual(res.name, 'Test API')

    async def test_request_put(self):
        with patch("aiohttp.ClientSession.put", new_callable=AsyncMock) as async_mock:
            self.request.body = {}
            self.request.method = 'PUT'

            async_mock.return_value = self.response

            session = aiohttp.ClientSession
            session.put = MagicMock()
            session.put.return_value.__aenter__.return_value.status = 200
            session.put.return_value.__aenter__.return_value.text.return_value = 'test content'
            res = await request(session, self.request)

        self.assertEqual(res.has_err, False)
        self.assertEqual(res.name, 'Test API')

    async def test_request_delete_error(self):
        with patch("aiohttp.ClientSession.delete", new_callable=AsyncMock) as async_mock:
            self.request.body = None
            self.request.method = 'DELETE'
            async_mock.return_value = self.response

            session = aiohttp.ClientSession
            session.delete = MagicMock()
            session.delete.return_value.__aenter__.return_value.status = 400
            session.delete.return_value.__aenter__.return_value.text.return_value = 'test content'
            res = await request(session, self.request)

        self.assertEqual(res.has_err, True)
        self.assertEqual(res.name, 'Test API')
