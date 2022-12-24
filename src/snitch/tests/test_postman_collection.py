from parsers.postman_parser import PostmanCollectionParser
import unittest
import sys
import os
current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_path + '/../')


class TestPostmanCollectionParser(unittest.TestCase):
    def setUp(self):
        pass

    def test_postman_collection_parser(self):
        pass
