import anyio
import asyncclick as click
import asyncio
from .parsers.postman_parser import PostmanFileParser
from .parsers.config_parser import ConfigParser
from .task_runners.health_check import run_health_check


@ click.command()
@ click.option('-p', '--path', help='Path of the configuration file')
async def run(path):
    try:
        # reading config file and parse data sychronously, coz there's only 1 config file
        # needs to read
        with open(path, 'r') as f:
            config = ConfigParser(f.read())

            if config.has_postman_collection:
                pp = PostmanFileParser(
                    config.collection_file_path, config.metadata)
        run_health_check(pp.requests)
    except Exception as e:
        click.echo(e)


if __name__ == '__main__':
    asyncio.run(run())
