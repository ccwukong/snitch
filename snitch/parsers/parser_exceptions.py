class InvalidPostmanCollectionVersion(Exception):
    def __init__(self, message) -> None:
        self.message = message


class InvalidOpenApiVersion(Exception):
    def __init__(self, message) -> None:
        self.message = message
