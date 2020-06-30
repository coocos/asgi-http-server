import unittest

from asgi.http import HttpRequest, HttpResponse
from asgi.exceptions import HttpRequestParsingException


class TestHttpRequest(unittest.TestCase):
    def test_constructing_request_from_raw_string(self):

        request = HttpRequest.from_raw_request(
            (
                "GET / HTTP/1.1\r\n"
                "User-Agent: curl/7.54.0\r\n"
                "Host: localhost:8000\r\n"
                "Accept: */*\r\n"
                "\r\n"
            )
        )
        self.assertEqual(request.method, "GET")
        self.assertEqual(request.path, "/")
        self.assertDictEqual(
            request.headers,
            {"user-agent": "curl/7.54.0", "host": "localhost:8000", "accept": "*/*"},
        )

    def test_constructing_request_with_body(self):
        request = HttpRequest.from_raw_request(
            (
                "POST / HTTP/1.1\r\n"
                "User-Agent: curl/7.54.0\r\n"
                "Host: localhost:8000\r\n"
                "Content-Type: application/json\r\n"
                "Accept: */*\r\n"
                "Content-Length: 8\r\n"
                "\r\n"
                '{"id":1}'
            )
        )
        self.assertEqual(request.method, "POST")
        self.assertEqual(request.path, "/")
        self.assertDictEqual(
            request.headers,
            {
                "user-agent": "curl/7.54.0",
                "host": "localhost:8000",
                "accept": "*/*",
                "content-type": "application/json",
                "content-length": "8",
            },
        )
        self.assertEqual(request.body, '{"id":1}')

    def test_that_parsing_invalid_request_raises_exception(self):

        with self.assertRaises(HttpRequestParsingException):
            request = HttpRequest.from_raw_request(
                ("HTTP/1.1\r\n" "Host 8000\r\n" "\r\n")
            )


class TestHttpResponse(unittest.TestCase):
    def test_constructing_http_response(self):

        response = HttpResponse(200, {"server": "asgi-from-scratch/0.1"})
        self.assertEqual(response.status, 200)
        self.assertDictEqual(response.headers, {"server": "asgi-from-scratch/0.1"})

    def test_encoding_http_response_to_bytes(self):

        response = HttpResponse(200, {"server": "asgi-from-scratch/0.1"})
        self.assertEqual(
            response.encode(),
            (b"HTTP/1.0 200 OK\r\n" b"server: asgi-from-scratch/0.1\r\n" b"\r\n"),
        )
