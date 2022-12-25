from time import time
import requests
from ..logger import LogItem


async def run_idempotency_check(req) -> LogItem:
    try:
        start = time()
        if req.method == 'GET':
            res1 = requests.get(req.url, headers=req.headers)
            if res1.status_code >= 400:
                raise Exception()
            res2 = requests.get(req.url, headers=req.headers)
            if res2.status_code >= 400:
                raise Exception()

            is_idempotent = res1.text == res2.text
        elif req.method == 'POST':
            res1 = requests.post(
                req.url, headers=req.headers, json=req.body)
            if res1.status_code >= 400:
                raise Exception()
            res2 = requests.post(
                req.url, headers=req.headers, json=req.body)
            if res2.status_code >= 400:
                raise Exception()
            is_idempotent = res1.text == res2.text
        elif req.method == 'PUT':
            res1 = requests.put(
                req.url, headers=req.headers, json=req.body)
            if res1.status_code >= 400:
                raise Exception()
            res2 = requests.put(
                req.url, headers=req.headers, json=req.body)
            if res2.status_code >= 400:
                raise Exception()
            is_idempotent = res1.text == res2.text
        elif req.method == 'DELETE':
            res1 = requests.delete(req.url, headers=req.headers)
            if res1.status_code >= 400:
                raise Exception()
            res2 = requests.delete(req.url, headers=req.headers)
            if res2.status_code >= 400:
                raise Exception()
            is_idempotent = res1.text == res2.text
        end = time()

        return LogItem(False, end - start, f'Idempotent: {is_idempotent}.', req.name)
    except Exception as e:
        end = time()
        return LogItem(True, end - start, f'Error. Idempotency untestable.', req.name)
