from snitch.task_runners.report_builder import ReportBuilder
import unittest
from unittest.mock import patch


class TestReportBuilder(unittest.TestCase):
    def setUp(self):
        self.data = {
            'total': 100,
            'success': 50,
            'errors': 50,
            'responses': [{'message': 'test message'}]
        }
        self.report_builder = ReportBuilder(self.data)

    def test_header(self):
        with patch("snitch.task_runners.report_builder.datetime") as mock:
            mock.now.return_value = 123
            self.assertEqual(self.report_builder.header,
                             f"Datetime: 123{self.report_builder.newline}Total APIs checked: 100{self.report_builder.newline}Success: 50{self.report_builder.newline}Errors: 50{self.report_builder.newline}Success rate: 50.00%")

    def test_conetnt(self):
        self.assertEqual(self.report_builder.content,
                         f"test message{self.report_builder.newline*2}")

    def test_other(self):
        self.assertEqual(self.report_builder.newline, '\n')
        self.assertEqual(self.report_builder.divider, f"{'-' * 50}")
