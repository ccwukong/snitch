import anyio
import asyncclick as click
import asyncio
import os
from time import time
from datetime import datetime
import uuid
from .parsers.postman_parser import PostmanFileParser
from .parsers.openapi_parser import OpenApiParser
from .parsers.config_parser import ConfigParser
from .task_runners.health_check import run_health_check


@ click.command()
@ click.option('-p', '--path', help='Path of the configuration file')
@ click.option('-o', '--output', help='Store the results on your device', default='')
async def run(path, output):
    try:
        # reading config file and parse data sychronously, coz there's only 1 config file
        # needs to read
        with open(path, 'r') as f:
            config = ConfigParser(f.read())
            requests = []

            if config.has_postman_collection:
                pp = PostmanFileParser(
                    config.collection_file_path, config.collection_metadata)
                requests.extend(pp.requests)
                # run health check and API validation, and handle the result

            if config.has_openapi:
                op = OpenApiParser(
                    config.openapi_file_path, config.openapi_metadata)
                requests.extend(op.requests)

            if requests:
                click.echo(click.style('Running Health check ...', fg='green'))
                res = await run_health_check(requests)
                if output:
                    if os.path.exists(output):
                        f = open(os.path.join(
                            output, f'hc_{time()}_{uuid.uuid4()}.txt'), 'w')
                        s = f"Datetime: {datetime.now()}\nTotal endpoints checked: {res['total']}\nSuccess: {res['success']}\nErrors: {res['errors']}\n\n\n"
                        for r in res['responses']:
                            s += f"{r}\n{'-'*50}\n"
                        f.write(s)
                        f.close()
                    else:
                        click.echo(click.style(
                            'Error: output destination directory doesn\'t exist.', fg='red'))

                click.echo('-'*50)
                for r in res['responses']:
                    click.echo(r)
                    click.echo('-'*50)
                click.echo(click.style(
                    f"Datetime: {datetime.now()}", fg='green'))
                click.echo(click.style(
                    f"Total endpoints checked: {res['total']}", fg='green'))
                click.echo(click.style(
                    f"Success: {res['success']}", fg='green'))
                click.echo(click.style(f"Errors: {res['errors']}", fg='red'))
                click.echo(click.style(
                    f"Success rate: {(res['success']/(res['success']+res['errors'])*100):.2f}%", fg='green'))

    except Exception as e:
        click.echo(e)


if __name__ == '__main__':
    asyncio.run(run())
