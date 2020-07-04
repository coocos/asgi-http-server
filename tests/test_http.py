import unittest

from asgi.http import HttpRequest, HttpResponse
from asgi import exceptions


class TestHttpRequest(unittest.TestCase):
    def test_deserializing_http_request_without_body(self):

        request = HttpRequest.deserialize(
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

    def test_deserializing_http_request_with_body(self):
        request = HttpRequest.deserialize(
            (
                "POST / HTTP/1.1\r\n"
                "User-Agent: curl/7.54.0\r\n"
                "Host: localhost:8000\r\n"
                "Content-Type: application/json\r\n"
                "Accept: */*\r\n"
                "Content-Length: 47\r\n"
                "\r\n"
                '{"first_name": "Paul", "last_name": "Atreides"}'
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
            request.body, '{"first_name": "Paul", "last_name": "Atreides"}'
        )

    def test_that_parsing_invalid_request_raises_exception(self):

        with self.assertRaises(exceptions.HttpRequestParsingException):
            request = HttpRequest.deserialize(("HTTP/1.1\r\n" "Host 8000\r\n" "\r\n"))


class TestHttpResponse(unittest.TestCase):
    def test_serializing_http_response_without_body(self):

        expected = b"HTTP/1.0 200 OK\r\n" b"content-type: text/plain\r\n" b"\r\n"
        response = HttpResponse(200, {"content-type": "text/plain"})
        self.assertEqual(response.serialize(), expected)

    def test_serializing_http_response_with_body(self):

        # TODO: Implement this
        pass
