import asyncclick as click
import asyncio
import os
import uuid
from datetime import date
from typing import List, Optional
from .parsers.postman_parser import PostmanCollectionParser
from .parsers.openapi_parser import OpenApiParser
from .parsers.config_parser import ConfigParser
from .task_runners.health_check import run_health_check
from .task_runners.idempotency_check import run_idempotency_check
from .task_runners.report_builder import ReportBuilder
from .scripts.generate_config_json_template import generate_config_json_template
from .task_runners.task import TaskType, TaskQueue, Task
from .parsers.request_model import Request


@click.command()
@click.option('-i', '--init', help='To create a new config.json template file, you need to provide a directory to store your config file', default='')
@click.option('-o', '--output', help='To specify an existing directory that stores task results on your device', default='')
@click.option('-p', '--path', help='To specify a path where stores the config JSON file')
@click.option('-t', '--task', help='To run a specific task, snitch will run all tasks if this flag is not provided', default='')
@click.option('-v', '--verbose', is_flag=True, help='To print API responses if -v or --verbose flag is provided')
async def run(path, output: Optional[str], init: Optional[str], task: Optional[str], verbose: Optional[bool]) -> None:
    try:
        if init:
            generate_config_json_template(init)
        else:
            if not path:
                raise Exception('Error. No -p or --path flag specified.')
            with open(path, 'r') as f:
                click.echo(click.style(
                    'Analyzing the configuration...\n', fg='yellow'))
                config = ConfigParser(f.read())
                reqs = []

                if config.has_postman_collection:
                    pp = PostmanCollectionParser(
                        config.collection_file_path, config.collection_metadata)

                    reqs.extend(pp.requests)
                    # run health check and API validation, and handle the result

                if config.has_openapi:
                    op = OpenApiParser(
                        config.openapi_file_path, config.openapi_metadata)
                    reqs.extend(op.requests)

                if reqs:
                    task_queue = TaskQueue()
                    if task:
                        match task:
                            case TaskType.HEALTH_CHECK.value:
                                task_queue.add_task(
                                    Task(run_health_task, (output, reqs, verbose)))
                            case TaskType.IDEMPOTENCY_CHECK.value:
                                task_queue.add_task(
                                    Task(run_idempotency_task, (output, reqs)))
                            case _: raise Exception(f'Error. \'{task}\' is an invalid task flag.')
                    else:
                        task_queue.add_task(
                            Task(run_health_task, (output, reqs, verbose)))
                        task_queue.add_task(
                            Task(run_idempotency_task, (output, reqs)))

                    while task_queue:
                        t = task_queue.pop_task()
                        await t.task(*t.args)
                else:
                    raise Exception('Error. No APIs available to check.')

    except Exception as e:
        click.echo(click.style(e, fg='red'))


async def run_health_task(output: str, requests: List[Request], verbose: bool) -> None:
    click.echo(click.style(
        'Running Health check ...', fg='yellow'))
    res = await run_health_check(requests, verbose)
    report_builder = ReportBuilder(res)
    report_builder.print_divider()
    report_builder.print_newline()
    report_builder.print_content()
    report_builder.print_divider()
    report_builder.print_summary()

    if output:
        if os.path.exists(output):
            f = open(os.path.join(
                output, generate_file_name('health_check')), 'w')

            f.write(report_builder.header)
            f.write(report_builder.newline)
            f.write(report_builder.divider)
            f.write(report_builder.newline * 2)
            f.write(report_builder.content)
            f.close()
        else:
            click.echo(
                click.style(
                    'Error: The output destination directory doesn\'t exist.',
                    fg='red'))


async def run_idempotency_task(output: str, requests: List[Request]) -> None:
    click.echo(click.style(
        '\nRunning Idempotency check, it will take longer...', fg='yellow'))
    idem_responses = []
    for re in requests:
        res = await run_idempotency_check(re)
        idem_responses.append(res)

    res = {}

    total = len(idem_responses)

    success = len(
        [i for i in idem_responses if not i['error']])
    res['total'] = total
    res['success'] = success
    res['errors'] = total - success
    res['responses'] = idem_responses

    report_builder = ReportBuilder(res)

    report_builder.print_divider()
    report_builder.print_newline()
    report_builder.print_content()
    report_builder.print_divider()
    report_builder.print_summary()

    if output:
        if os.path.exists(output):
            f = open(os.path.join(
                output, generate_file_name('idempotency')), 'w')

            f.write(report_builder.header)
            f.write(report_builder.newline)
            f.write(report_builder.divider)
            f.write(report_builder.newline * 2)
            f.write(report_builder.content)
            f.close()
        else:
            click.echo(
                click.style(
                    'Error: The output destination directory doesn\'t exist.',
                    fg='red'))


def generate_file_name(type: str) -> str:
    return f'{type}_{date.today().strftime("%Y_%m_%d")}_{uuid.uuid4()}.log'


if __name__ == '__main__':
    asyncio.run(run())
