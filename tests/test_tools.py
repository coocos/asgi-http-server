import unittest

from asgi.tools import HttpRequest


class TestHttpRequest(unittest.TestCase):
    def test_constructing_request_from_raw_string(self):

        request = HttpRequest.from_raw_request(
            """
            GET / HTTP/1.1\r\n
            """
        )
        self.assertEqual(request.method, "GET")
        self.assertEqual(request.path, "/")
