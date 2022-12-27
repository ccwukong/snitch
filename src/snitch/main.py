import asyncclick as click
import os
from time import time
import uuid
from .parsers.postman_parser import PostmanCollectionParser
from .parsers.openapi_parser import OpenApiParser
from .parsers.config_parser import ConfigParser
from .task_runners.health_check import run_health_check
from .task_runners.idempotency_check import run_idempotency_check
from .task_runners.report_builder import ReportBuilder
from .scripts.generate_config_json_template import generate_config_json_template


@click.command()
@click.option('-i', '--init', help='Initiate a new config.json template file, you need to provide a directory to store your config file', default='')
@click.option('-o', '--output', help='Store the results on your device', default='')
@click.option('-p', '--path', help='Path of the configuration file')
@click.option('-t', '--task', help='Run a specific task, snitch will run all tasks if this flag is not specified', default='')
@click.option('-v', '--verbose', is_flag=True, help='Print API responses if -v or --verbose flag is specified')
async def run(path, output, init, task, verbose):
    try:
        if init:
            generate_config_json_template(init)
        else:
            if not path:
                raise Exception('Error. No -p or --path flag specified.')
            with open(path, 'r') as f:
                click.echo(click.style(
                    'Analyzing configuration ...\n', fg='yellow'))
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
                    if task:
                        match task:
                            case 'hc': await run_health_task(output, reqs, verbose)
                            case 'id': await run_idempotency_task(output, reqs)
                            case _: raise Exception(f'Error. {task} is an invalid task flag.')
                    else:
                        await run_health_task(output, reqs, verbose)
                        await run_idempotency_task(output, reqs)
                else:
                    raise Exception('Error. No APIs available to check.')

    except Exception as e:
        click.echo(click.style(e, fg='red'))


async def run_health_task(output: str, reqs: list, verbose: bool):
    click.echo(click.style(
        'Running Health check ...', fg='yellow'))
    res = await run_health_check(reqs, verbose)
    report_builder = ReportBuilder(res)
    report_builder.print_divider()
    report_builder.print_newline()
    report_builder.print_content()
    report_builder.print_divider()
    report_builder.print_summary()

    if output:
        if os.path.exists(output):
            f = open(os.path.join(
                output, generate_file_name('health_check_check')), 'w')

            f.write(report_builder.header)
            f.write(report_builder.newline)
            f.write(report_builder.divider)
            f.write(report_builder.newline * 2)
            f.write(report_builder.content)
            f.close()
        else:
            click.echo(
                click.style(
                    'Error: Output destination directory doesn\'t exist.',
                    fg='red'))


async def run_idempotency_task(output: str, reqs: list):
    click.echo(click.style(
        '\nRunning Idempotency check, it will take longer time ...', fg='yellow'))
    idem_responses = []
    for re in reqs:
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
                    'Error: Output destination directory doesn\'t exist.',
                    fg='red'))


def generate_file_name(type: str) -> str:
    return f'{type}_{time()}_{uuid.uuid4()}.log'


if __name__ == '__main__':
    run()
