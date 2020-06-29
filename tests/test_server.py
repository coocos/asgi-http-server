import asyncio
import unittest

from asgi.server import process_http_request
from asgi.tools import HttpRequest

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

        process = process_http_request(StreamReader(request))
        result = asyncio.run(process)
        self.assertEqual(result, HttpRequest(
            "GET",
            "/",
            {
                "host": "localhost:8000",
                "user-agent": "Archer/1.0.0",
                "accept-encoding": "gzip/deflate"
            }
        ))