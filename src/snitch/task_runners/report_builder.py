import asyncclick as click
from datetime import datetime


class ReportBuilder:
    '''
    ReportBuilder builds formatted report strings, it won't print anything on command line
    '''

    def __init__(self, data: dict):
        self.__data = data

    @property
    def header(self) -> str:
        return f"Datetime: {datetime.now()}{self.newline}Total APIs checked: {self.__data['total']}{self.newline}Success: {self.__data['success']}{self.newline}Errors: {self.__data['errors']}{self.newline}Success rate: {self.__data['success'] / self.__data['total'] * 100:.2f}%"

    @property
    def content(self) -> str:
        s = ''
        if 'responses' in self.__data:
            for r in self.__data['responses']:
                s += f"{r['message']}{self.newline * 2}"
            return s
        else:
            return ''

    @property
    def newline(self) -> str:
        return '\n'

    @property
    def divider(self) -> str:
        return f"{'-' * 50}"

    def print_newline(self):
        click.echo(self.newline)

    def print_divider(self):
        click.echo(self.divider)

    def print_content(self):
        for r in self.__data['responses']:
            if not r['error']:
                click.echo(r['message'])
            else:
                click.echo(click.style(
                    r['message'], fg='red'))
            self.print_newline()

    def print_summary(self):
        click.echo(click.style(
            f"Datetime: {datetime.now()}", fg='green'))
        click.echo(click.style(
            f"Total APIs checked: {self.__data['total']}", fg='green'))
        click.echo(click.style(
            f"Success: {self.__data['success']}", fg='green'))
        click.echo(click.style(f"Errors: {self.__data['errors']}", fg='red'))
        click.echo(click.style(
            f"Success rate: {self.__data['success'] / self.__data['total'] * 100:.2f}%", fg='green'))
