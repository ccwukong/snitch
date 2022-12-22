import json
import aiohttp
from json.decoder import JSONDecodeError


async def run_health_check(requests):
    # create different tasks to send request asynchronousely using coroutine
    # to increase concurrency.
    # we use aiohttp here, so no need to mix coroutines with the threading pool
    async with aiohttp.ClientSession() as s:
        res = await get_all_requests(s, requests)

    print(res)


async def request(session, request):
    try:
        if request.method == 'GET':
            async with session.get(request.url, headers=request.headers) as response:
                return await response.json()
        elif request.method == 'POST':
            async with session.post(request.url, headers=request.headers, data=json.dumps(request.body)) as response:
                return await response.text()
    except Exception as e:
        raise e


async def get_all_requests(session, requests):
    try:
        tasks = []

        for req in requests:
            tasks.append(asyncio.create_task(request(session, req)))

        return await asyncio.gather(*tasks)
    except Exception as e:
        raise e
