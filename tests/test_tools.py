import unittest

from asgi.tools import HttpRequest
from asgi.exceptions import HttpRequestParsingException


class TestHttpRequest(unittest.TestCase):
    def test_constructing_request_from_raw_string(self):

        request = HttpRequest.from_raw_request(
            """
            GET / HTTP/1.1\r\n
            User-Agent: curl/7.54.0\r\n
            Host: localhost:8000\r\n
            Accept: */*\r\n
            \r\n
            """
        )
        self.assertEqual(request.method, "GET")
        self.assertEqual(request.path, "/")
        self.assertDictEqual(
            request.headers,
            {"user-agent": "curl/7.54.0", "host": "localhost:8000", "accept": "*/*"},
        )

    def test_that_parsing_invalid_request_raises_exception(self):

        with self.assertRaises(HttpRequestParsingException):
            request = HttpRequest.from_raw_request(
                """
                HTTP/1.1\r\n
                Host 8000\r\n
                \r\n
                """
            )
