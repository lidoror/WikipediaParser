import unittest
import requests
from unittest.mock import patch
import utils


@patch('requests.get')
class TestGetPageDate(unittest.TestCase):

    def test_status_code(self, mock_get):
        mock_get.return_value.status_code = 200
        response = requests.get('https://test-site.com')
        self.assertEqual(response.status_code, 200)


class TestParseHtmlWebsite(unittest.TestCase):

    def test_parsed_data(self):
        html = '<html><body><h1>Test</h1></body></html>'
        parsed_html = utils.parse_html_website(html)
        self.assertEqual(parsed_html.h1.text, 'Test')
