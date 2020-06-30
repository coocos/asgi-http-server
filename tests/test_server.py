import asyncio
import unittest

from asgi.server import read_http_request
from asgi.http import HttpRequest


class StreamReader:
    """Fake implementation of asyncio.streams.StreamReader"""

    def __init__(self, stream: bytearray):
        self._stream = stream

    async def read(self, bytes_: int = 0) -> bytes:
        next_bytes = self._stream[:bytes_]
        self._stream = self._stream[bytes_:]
        return next_bytes


class TestHttpRequestProcessing(unittest.TestCase):
    def test_processing_http_request_with_no_body(self):

        request = (
            b"GET / HTTP/1.1\r\n"
            b"Host: localhost:8000\r\n"
            b"User-Agent: Archer/1.0.0\r\n"
            b"Accept-Encoding: gzip/deflate\r\n"
            b"\r\n"
        )

        process = read_http_request(StreamReader(request))
        result = asyncio.run(process)
        self.assertEqual(
            result,
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

    def test_processing_http_request_with_body(self):

        request = (
            b"POST /api/v1/ HTTP/1.1\r\n"
            b"Host: localhost:8000\r\n"
            b"User-Agent: Archer/1.0.0\r\n"
            b"Accept-Encoding: gzip, deflate\r\n"
            b"Connection: keep-alive\r\n"
            b"Content-Type: application/json\r\n"
            b"Content-Length: 47\r\n"
            b"\r\n"
            b'{"first_name": "Paul", "last_name": "Atreides"}'
        )

        process = read_http_request(StreamReader(request))
        result = asyncio.run(process)
        self.assertEqual(
            result,
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
