import anyio
import asyncclick as click
import json
from json.decoder import JSONDecodeError
from src.parsers.postman_parser import PostmanFileParser
from src.parsers.config_parser import ConfigParser
import asyncio
import aiohttp


async def request(session, request):
    try:
        if request.method == 'GET':
            async with session.get(request.url, headers=request.headers) as response:
                print(await response.json())
                return await response.json()
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


@ click.command()
@ click.option('-p', '--path', help='Path of the configuration file')
async def run(path):
    try:
        # reading config file and parse data sychronously, coz there's only 1 config file
        # needs to read
        with open('./testdata/config.json', 'r') as f:
            config = ConfigParser(f.read())
            if config.has_postman_collection:
                pp = PostmanFileParser(
                    config.collection_file_path, config.metadata)

        # create different tasks to send request asynchronousely using coroutine
        # to increase concurrency.
        # we use aiohttp here, so no need to mix coroutines with the threading pool
        async with aiohttp.ClientSession() as s:
            res = await get_all_requests(s, pp.requests)

        print(res)
    except Exception as e:
        click.echo(e)


if __name__ == '__main__':
    asyncio.run(run())
