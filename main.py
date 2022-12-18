import click
import json
from json.decoder import JSONDecodeError
from src.parsers.postman_parser import PostmanFileParser
from src.parsers.config_parser import ConfigParser


@click.command()
@click.option('-p', '--path', help='Path of the configuration file')
def run(path):
    try:
        with open(path, 'r') as f:
            config = ConfigParser(f.read())
            pp = PostmanFileParser(config.postman_collection_file_path)
            print(pp.endpoints)
    except JSONDecodeError as e:
        click.echo(e)
    except FileNotFoundError as e:
        click.echo(e)


if __name__ == '__main__':
    run()
