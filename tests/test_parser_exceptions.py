from snitch.parsers.parser_exceptions import InvalidPostmanCollectionVersion, InvalidOpenApiVersion
import unittest


class TestExceptions(unittest.TestCase):
    def test_InvalidPostmanCollectionVersion(self):
        err_msg = 'Error. snitch requires Postman collection version >= 2.0'
        e = InvalidPostmanCollectionVersion(
            err_msg)

        self.assertEqual(e.message, err_msg)

        try:
            raise e
        except Exception as err:
            self.assertEqual(e.message, err_msg)

        err_msg = 'Error. snitch requires Open API version >= 3.0.0'
        e = InvalidOpenApiVersion(
            err_msg)

        self.assertEqual(e.message, err_msg)

        try:
            raise e
        except Exception as err:
            self.assertEqual(e.message, err_msg)
