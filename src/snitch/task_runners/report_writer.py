import asyncclick as click


class ReportWriter:
    def __init__(self, data):
        if type(data) == list:
            # handle idempotency check here
            self.__data = data
        else:
            # handle health check data here
            pass

    @property
    def header(self):
