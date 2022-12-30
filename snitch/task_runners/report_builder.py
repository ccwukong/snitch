import asyncclick as click
from datetime import datetime
from typing import Dict


class ReportBuilder:
    '''
    ReportBuilder builds formatted report strings
    '''

    def __init__(self, data: Dict):
        self.__data = data

    @property
    def header(self) -> str:
        return f"Datetime: {datetime.now()}{self.newline}Total APIs checked: {self.__data['total']}{self.newline}" + \
            f"Success: {self.__data['success']}{self.newline}Errors: {self.__data['errors']}{self.newline}" + \
            f"Success rate: {self.__data['success'] / self.__data['total'] * 100:.2f}%"

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

    def print_newline(self) -> None:
        click.echo(self.newline)

    def print_divider(self) -> None:
        click.echo(self.divider)

    def print_content(self) -> None:
        for r in self.__data['responses']:
            if not r['error']:
                click.echo(r['message'])
            else:
                click.echo(click.style(
                    r['message'], fg='red'))
            self.print_newline()

    def print_summary(self) -> None:
        click.echo(click.style(
            f"Datetime: {datetime.now()}", fg='green'))
        click.echo(click.style(
            f"Total APIs checked: {self.__data['total']}", fg='green'))
        click.echo(click.style(
            f"Success: {self.__data['success']}", fg='green'))
        click.echo(click.style(f"Errors: {self.__data['errors']}", fg='red'))
        click.echo(click.style(
            f"Success rate: {self.__data['success'] / self.__data['total'] * 100:.2f}%", fg='green'))
