import anyio
import asyncclick as click
import json
from json.decoder import JSONDecodeError
from src.parsers.postman_parser import PostmanFileParser
from src.parsers.config_parser import ConfigParser
import asyncio
import aiohttp


async def request(i):
    async with aiohttp.ClientSession() as session:
        async with session.get('http://python.org') as response:
            print(i)
            return await response.text()


@click.command()
@click.option('-p', '--path', help='Path of the configuration file')
async def run(path):
    try:
        with open('./testdata/config.json', 'r') as f:
            config = ConfigParser(f.read())
            if config.has_postman_collection:
                pp = PostmanFileParser(
                    config.collection_file_path, config.metadata)
                print(pp.requests)
    except Exception as e:
        click.echo(e)
    # tasks = []

    # for i in range(10):
    #     tasks.append(request(i))

    # await asyncio.wait(tasks)

if __name__ == '__main__':
    asyncio.run(run())
