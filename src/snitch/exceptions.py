class InvalidJSONError(Exception):
    def __init__(self):
        self.message = "Error. Invalid JSON file."
