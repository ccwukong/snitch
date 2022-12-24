class InvalidPostmanCollectionVersion(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class InvalidOpenApiVersion(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
