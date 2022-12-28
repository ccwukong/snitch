import aiohttp
import asyncio
from time import time
from ..logger import LogItem
from ..parsers.request_model import Request


async def run_health_check(requests: list[Request], verbose: bool = False) -> dict:
    async with aiohttp.ClientSession() as s:
        res = await get_all_requests(s, requests)

    status = {}
    status['total'] = len(res)
    status['errors'] = len([i for i in res if i.has_err])
    status['success'] = status['total'] - status['errors']
    status['responses'] = [
        {'error': i.has_err,
         'message':
         f'Name: {i.name}\nError: {i.has_err}\nLatency: {i.run_time}s' + (f'\nResponse: {i.message}' if verbose else '')}
        for i in res]

    return status


async def request(session, request) -> LogItem:
    try:
        start = time()
        if request.method == 'GET':
            async with session.get(request.url, headers=request.headers) as response:
                if response.status >= 400:
                    raise Exception(f'{response.status} - {response.content}')
                msg = await response.text()
        elif request.method == 'POST':
            async with session.post(request.url, headers=request.headers, json=request.body) as response:
                if response.status >= 400:
                    raise Exception(f'{response.status} - {response.content}')
                msg = await response.text()
        elif request.method == 'PUT':
            async with session.put(request.url, headers=request.headers, json=request.body) as response:
                if response.status >= 400:
                    raise Exception(f'{response.status} - {response.content}')
                msg = await response.text()
        elif request.method == 'DELETE':
            async with session.delete(request.url, headers=request.headers) as response:
                if response.status >= 400:
                    raise Exception(f'{response.status} - {response.content}')
                msg = await response.text()
        end = time()

        return LogItem(False, end - start, msg, request.name)
    except Exception as e:
        end = time()
        return LogItem(True, end - start, e, request.name)


async def get_all_requests(session, requests) -> list[LogItem]:
    try:
        tasks = []
        for req in requests:
            tasks.append(asyncio.create_task(request(session, req)))

        result = await asyncio.gather(*tasks)

        return result
    except Exception as e:
        raise e
