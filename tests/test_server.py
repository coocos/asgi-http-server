import asyncio
import unittest

from asgi.http import HttpRequest, HttpResponse


class StreamReader:
    """Fake implementation of asyncio.streams.StreamReader"""

    def __init__(self, stream: bytearray):
        self._stream = stream

    async def read(self, bytes_: int = 0) -> bytes:
        next_bytes = self._stream[:bytes_]
        self._stream = self._stream[bytes_:]
        return next_bytes


class TestHttpRequest(unittest.TestCase):
    def test_deserializing_http_request_without_body(self):

        raw = (
            "GET / HTTP/1.1\r\n"
            "Host: localhost:8000\r\n"
            "User-Agent: Archer/1.0.0\r\n"
            "Accept-Encoding: gzip/deflate\r\n"
            "\r\n"
        )

        request = HttpRequest.deserialize(raw)
        self.assertEqual(
            request,
            HttpRequest(
                "GET",
                "/",
                {
                    "host": "localhost:8000",
                    "user-agent": "Archer/1.0.0",
                    "accept-encoding": "gzip/deflate",
                },
            ),
        )

    def test_deserializing_http_request_with_body(self):

        raw = (
            "POST /api/v1/ HTTP/1.1\r\n"
            "Host: localhost:8000\r\n"
            "User-Agent: Archer/1.0.0\r\n"
            "Accept-Encoding: gzip, deflate\r\n"
            "Connection: keep-alive\r\n"
            "Content-Type: application/json\r\n"
            "Content-Length: 47\r\n"
            "\r\n"
            '{"first_name": "Paul", "last_name": "Atreides"}'
        )

        request = HttpRequest.deserialize(raw)
        self.assertEqual(
            request,
            HttpRequest(
                "POST",
                "/api/v1/",
                {
                    "host": "localhost:8000",
                    "user-agent": "Archer/1.0.0",
                    "accept-encoding": "gzip, deflate",
                    "connection": "keep-alive",
                    "content-type": "application/json",
                    "content-length": "47",
                },
                '{"first_name": "Paul", "last_name": "Atreides"}',
            ),
        )


class TestHttpResponse(unittest.TestCase):
    def test_serializing_http_response_without_body(self):

        expected = b"HTTP/1.0 200 OK\r\n" b"content-type: text/plain\r\n" b"\r\n"
        response = HttpResponse(200, {"content-type": "text/plain"})
        self.assertEqual(response.serialize(), expected)
