import unittest

from asgi.http import HttpRequest, HttpResponse
from asgi import exceptions


class TestHttpRequest(unittest.TestCase):
    def test_deserializing_http_request_without_body(self):

        request = HttpRequest.deserialize(
            (
                b"GET / HTTP/1.0\r\n"
                b"User-Agent: curl/7.54.0\r\n"
                b"Host: localhost:8000\r\n"
                b"Accept: */*\r\n"
                b"\r\n"
            )
        )
        self.assertEqual(request.method, "GET")
        self.assertEqual(request.path, "/")
        self.assertDictEqual(
            request.headers,
            {"user-agent": "curl/7.54.0", "host": "localhost:8000", "accept": "*/*"},
        )

    def test_deserializing_http_request_with_body(self):
        request = HttpRequest.deserialize(
            (
                b"POST / HTTP/1.0\r\n"
                b"User-Agent: curl/7.54.0\r\n"
                b"Host: localhost:8000\r\n"
                b"Content-Type: application/json\r\n"
                b"Accept: */*\r\n"
                b"Content-Length: 47\r\n"
                b"\r\n"
                b'{"first_name": "Paul", "last_name": "Atreides"}'
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
                "content-length": "47",
            },
        )
        self.assertEqual(
            request.body, b'{"first_name": "Paul", "last_name": "Atreides"}'
        )

    def test_that_parsing_invalid_request_raises_exception(self):

        with self.assertRaises(exceptions.HttpRequestParsingException):
            request = HttpRequest.deserialize((b"HTTP/1.0\r\nHost 8000\r\n\r\n"))


class TestHttpResponse(unittest.TestCase):
    def test_serializing_http_response_without_body(self):

        expected = b"HTTP/1.0 200 OK\r\n" b"content-type: text/plain\r\n" b"\r\n"
        response = HttpResponse(200, {"content-type": "text/plain"})
        self.assertEqual(response.serialize(), expected)
