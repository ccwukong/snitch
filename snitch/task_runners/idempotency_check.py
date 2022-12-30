from time import time
import requests
from typing import Dict
from ..parsers.request_model import Request
from ..logger import LogItem


async def run_idempotency_check(req: Request) -> Dict[str, str]:
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

        log = LogItem(False, end - start,
                      f'{is_idempotent}', req.name)

        return {'error': log.has_err,
                'message':
                f'Name: {log.name}\nError: {log.has_err}\nLatency: {log.run_time}s\nIdempotent: {log.message}'}

    except Exception as e:
        end = time()
        log = LogItem(True, end - start,
                      f'Untestable', req.name)

        return {'error': log.has_err,
                'message':
                f'Name: {log.name}\nError: {log.has_err}\nLatency: {log.run_time}s\nIdempotent: {log.message}'}
