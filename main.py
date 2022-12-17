import click
import json
from src.parsers.postman_parser import postman_parse


@click.command()
@click.option('-p', '--path', help='Path of the configuration file')
def run(path):
    try:
        f = open(path, 'r')
        config = postman_parse(f.read())
        print(config)
        f.close()
    except json.decoder.JSONDecodeError as e:
        click.echo(e)


if __name__ == '__main__':
    run()
