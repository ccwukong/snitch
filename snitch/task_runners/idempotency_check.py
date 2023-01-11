import asyncio
from time import time
import requests
from typing import Dict, List
from snitch.parsers.request_model import Request
from snitch.logger import LogItem


def run_idempotency_check(request: Request, verbose: bool = False) -> Dict[str, str]:
    try:
        start = time()
        has_err = False
        if request.method == 'GET':
            res1 = requests.get(request.url, headers=request.headers)
            res2 = requests.get(request.url, headers=request.headers)
        elif request.method == 'POST':
            res1 = requests.post(
                request.url, headers=request.headers, json=request.body)
            res2 = requests.post(
                request.url, headers=request.headers, json=request.body)
        elif request.method == 'PUT':
            res1 = requests.put(
                request.url, headers=request.headers, json=request.body)
            res2 = requests.put(
                request.url, headers=request.headers, json=request.body)
        elif request.method == 'DELETE':
            res1 = requests.delete(request.url, headers=request.headers)
            res2 = requests.delete(request.url, headers=request.headers)

        is_idempotent = res1.text == res2.text
        end = time()
        log = LogItem(False, end - start,
                      f'{is_idempotent}', request.name)

        verbose_msg = ''
        if verbose:
            verbose_msg = f'\nRequest: {request.__dict__}\nFirst response: {res1.text}\nSecond response: {res2.text}'

        if res1.status_code >= 400 or res2.status_code >= 400:
            raise Exception(verbose_msg)

        return {'error': log.has_err,
                'message':
                f'Name: {log.name}\nError: {log.has_err}\nLatency: {log.run_time}s\nIdempotent: {log.message}' + verbose_msg}

    except Exception as e:
        end = time()
        log = LogItem(True, end - start,
                      f'Untestable', request.name)
        return {'error': log.has_err,
                'message':
                f'Name: {log.name}\nError: {log.has_err}\nLatency: {log.run_time}s\nIdempotent: {log.message}' + str(e)}


# TODO: bad practice, parameter drilling
async def run_all_idempotency_check(requests: List[Request], verbose: bool = False) -> List[Dict]:
    loop = asyncio.get_event_loop()

    futures = []
    for r in requests:
        futures.append(loop.run_in_executor(
            None, run_idempotency_check, r, verbose))

    return await asyncio.gather(*futures)
