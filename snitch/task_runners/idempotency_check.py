import asyncio
from time import time
import requests
from typing import Dict, List
from ..parsers.request_model import Request
from ..logger import LogItem


def run_idempotency_check(request: Request) -> Dict[str, str]:
    try:
        start = time()
        if request.method == 'GET':
            res1 = requests.get(request.url, headers=request.headers)
            if res1.status_code >= 400:
                raise Exception()
            res2 = requests.get(request.url, headers=request.headers)
            if res2.status_code >= 400:
                raise Exception()
            is_idempotent = res1.text == res2.text
        elif request.method == 'POST':
            res1 = requests.post(
                request.url, headers=request.headers, json=request.body)
            if res1.status_code >= 400:
                raise Exception()
            res2 = requests.post(
                request.url, headers=request.headers, json=request.body)
            if res2.status_code >= 400:
                raise Exception()
            is_idempotent = res1.text == res2.text
        elif request.method == 'PUT':
            res1 = requests.put(
                request.url, headers=request.headers, json=request.body)
            if res1.status_code >= 400:
                raise Exception()
            res2 = requests.put(
                request.url, headers=request.headers, json=request.body)
            if res2.status_code >= 400:
                raise Exception()
            is_idempotent = res1.text == res2.text
        elif request.method == 'DELETE':
            res1 = requests.delete(request.url, headers=request.headers)
            if res1.status_code >= 400:
                raise Exception()
            res2 = requests.delete(request.url, headers=request.headers)
            if res2.status_code >= 400:
                raise Exception()
            is_idempotent = res1.text == res2.text
        end = time()

        log = LogItem(False, end - start,
                      f'{is_idempotent}', request.name)

        return {'error': log.has_err,
                'message':
                f'Name: {log.name}\nError: {log.has_err}\nLatency: {log.run_time}s\nIdempotent: {log.message}'}

    except Exception as e:
        end = time()
        log = LogItem(True, end - start,
                      f'Untestable', request.name)

        return {'error': log.has_err,
                'message':
                f'Name: {log.name}\nError: {log.has_err}\nLatency: {log.run_time}s\nIdempotent: {log.message}'}


async def run_all_idempotency_check(requests: List[Request]) -> List[Dict]:
    loop = asyncio.get_event_loop()

    futures = []
    for r in requests:
        futures.append(loop.run_in_executor(None, run_idempotency_check, r))

    return await asyncio.gather(*futures)
