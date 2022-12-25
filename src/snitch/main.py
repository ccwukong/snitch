import asyncclick as click
import os
from time import time
from datetime import datetime
import uuid
from .parsers.postman_parser import PostmanCollectionParser
from .parsers.openapi_parser import OpenApiParser
from .parsers.config_parser import ConfigParser
from .task_runners.health_check import run_health_check
from .task_runners.idempotency_check import run_idempotency_check
from .logger import LogItem


@click.command()
@click.option('-p', '--path', help='Path of the configuration file')
@click.option('-o', '--output', help='Store the results on your device', default='')
async def run(path, output):
    try:
        # reading config file and parse data sychronously, coz there's only 1 config file
        # needs to read
        with open(path, 'r') as f:
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
                click.echo(click.style('Running Health check ...', fg='green'))
                res = await run_health_check(reqs)
                if output:
                    if os.path.exists(output):
                        f = open(os.path.join(
                            output, generate_file_name('health_check_check')), 'w')

                        f.write(generate_health_check_report(res))
                        f.close()
                    else:
                        click.echo(
                            click.style(
                                'Error: output destination directory doesn\'t exist.',
                                fg='red'))
                print_health_check_report(res)

                click.echo(click.style(
                    '\nRunning Idempotency check, it will take longer time ...', fg='green'))

                idem_reqs = []
                for re in reqs:
                    res = await run_idempotency_check(re)
                    idem_reqs.append(res)
                total = len(idem_reqs)
                success = len([i for i in idem_reqs if not i.has_err])
                errs = total - success
                print_idempotency_report(idem_reqs, success, total, errs)

                if output:
                    if os.path.exists(output):
                        f = open(os.path.join(
                            output, generate_file_name('idempotency')), 'w')

                        f.write(generate_idempotency_check_report(
                            idem_reqs, success, total, errs))
                        f.close()
                    else:
                        click.echo(
                            click.style(
                                'Error: output destination directory doesn\'t exist.',
                                fg='red'))
    except Exception as e:
        click.echo(click.style(e, fg='red'))


def generate_health_check_report(res) -> str:
    s = f"Datetime: {datetime.now()}\nTotal APIs checked: {res['total']}\nSuccess: {res['success']}\nErrors: {res['errors']}\n\n\n"
    for r in res['responses']:
        s += f"{r['message']}\n{'-' * 50}\n"
    return s


def generate_idempotency_check_report(reqs: list[LogItem], success: int, total: int, errors: int) -> str:
    s = f"Datetime: {datetime.now()}\nTotal APIs checked: {total}\nSuccess: {success}\nErrors: {errors}\n\n\n"
    for r in reqs:
        msg = f'Name: {r.name}\nError: {r.has_err}\nLatency: {r.run_time}s\n{r.message}'
        s += f"{msg}\n{'-' * 50}\n"
    return s


def generate_file_name(type: str) -> str:
    return f'{type}_{time()}_{uuid.uuid4()}.log'


def print_health_check_report(res) -> None:
    click.echo('-' * 50)
    for r in res['responses']:
        if not r['error']:
            click.echo(r['message'])
        else:
            click.echo(click.style(
                r['message'], fg='red'))
        print('\n')

    click.echo('-' * 50)
    click.echo(click.style(
        f"Datetime: {datetime.now()}", fg='green'))
    click.echo(click.style(
        f"Total APIs checked: {res['total']}", fg='green'))
    click.echo(click.style(
        f"Success: {res['success']}", fg='green'))
    click.echo(click.style(f"Errors: {res['errors']}", fg='red'))
    click.echo(click.style(
        f"Success rate: {calc_success_perentage(res):.2f}%", fg='green'))


def calc_success_perentage(res) -> float:
    return res['success'] / (res['success'] + res['errors']) * 100


def print_idempotency_report(reqs: list[LogItem], success: int, total: int, errors: int) -> None:
    click.echo('-' * 50)
    for r in reqs:
        msg = f'Name: {r.name}\nError: {r.has_err}\nLatency: {r.run_time}s\n{r.message}'
        if not r.has_err:
            click.echo(msg)
        else:
            click.echo(click.style(msg, fg='red'))
        print('\n')

    click.echo('-' * 50)
    click.echo(click.style(
        f"Datetime: {datetime.now()}", fg='green'))
    click.echo(click.style(
        f"Total APIs checked: {total}", fg='green'))
    click.echo(click.style(
        f"Success: {success}", fg='green'))
    click.echo(click.style(f"Errors: {errors}", fg='red'))
    click.echo(click.style(
        f"Success rate: {success/total:.2f}%", fg='green'))


if __name__ == '__main__':
    run()
