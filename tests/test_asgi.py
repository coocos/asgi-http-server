import asyncio
import unittest

from asgi.http import HttpRequest, HttpResponse, AsgiHttpRequest, AsgiHttpResponse


class StreamReader:
    """Fake implementation of asyncio.streams.StreamReader"""

    def __init__(self, stream: bytearray):
        self._stream = stream

    async def read(self, bytes_: int = 0) -> bytes:
        next_bytes = self._stream[:bytes_]
        self._stream = self._stream[bytes_:]
        return next_bytes


class StreamWriter:
    """Fake implementation of asyncio.streams.StreamWriter"""

    def __init__(self):
        self.stream = bytearray()
        self.closed = False

    def write(self, data: bytes) -> None:
        self.stream += data

    def close(self) -> None:
        self.closed = True

    async def drain(self) -> None:
        pass

    async def wait_closed(self) -> None:
        pass


class TestAsgiHttpRequest(unittest.TestCase):
    def test_reading_scope(self):

        raw_request = (
            b"GET /api/v1/ HTTP/1.0\r\n"
            b"User-Agent: curl/7.54.0\r\n"
            b"Host: localhost:8000\r\n"
            b"\r\n"
        )
        request = AsgiHttpRequest(StreamReader(raw_request))
        scope = asyncio.run(request.scope())
        self.assertDictEqual(
            scope,
            {
                "type": "http",
                "asgi": {"version": "3.0", "spec_version": "2.0",},
                "http_version": "1.0",
                "method": "GET",
                "scheme": "http",
                "path": "/api/v1/",
                "query_string": "",
                "headers": [
                    [b"user-agent", b"curl/7.54.0"],
                    [b"host", b"localhost:8000"],
                ],
            },
        )

    def test_reading_entire_request(self):
        raw_request = (
            b"POST /api/v1/ HTTP/1.0\r\n"
            b"User-Agent: curl/7.54.0\r\n"
            b"Host: localhost:8000\r\n"
            b"Content-Type: application/json\r\n"
            b"Content-Length: 44\r\n"
            b"\r\n"
            b'{"first_name":"paul","last_name":"atreides"}'
        )

        async def read_request():
            request = AsgiHttpRequest(StreamReader(raw_request))
            scope = await request.scope()
            event = await request.read()
            return event

        scope = asyncio.run(read_request())
        self.assertDictEqual(
            scope,
            {
                "type": "http.request",
                "body": b'{"first_name":"paul","last_name":"atreides"}',
                "more_body": False,
            },
        )


class TestAsgiHttpResponse(unittest.TestCase):
    def test_writing_headers(self):
        message = {
            "type": "http.response.start",
            "status": 200,
            "headers": [
                [b"content-type", b"application/json"],
                [b"content-length", b"44"],
            ],
        }
        writer = StreamWriter()
        response = AsgiHttpResponse(writer)
        asyncio.run(response.write(message))
        self.assertEqual(
            writer.stream,
            (
                b"HTTP/1.0 200 OK\r\n"
                b"content-type: application/json\r\n"
                b"content-length: 44\r\n"
                b"\r\n"
            ),
        )

    def test_writing_headers_and_body(self):
        messages = [
            {
                "type": "http.response.start",
                "status": 200,
                "headers": [
                    [b"content-type", b"application/json"],
                    [b"content-length", b"44"],
                ],
            },
            {
                "type": "http.response.body",
                "body": b'{"first_name":"paul","last_name":"atreides"}',
                "more_body": False,
            },
        ]
        writer = StreamWriter()
        response = AsgiHttpResponse(writer)
        for message in messages:
            asyncio.run(response.write(message))
        self.assertEqual(
            writer.stream,
            (
                b"HTTP/1.0 200 OK\r\n"
                b"content-type: application/json\r\n"
                b"content-length: 44\r\n"
                b"\r\n"
                b'{"first_name":"paul","last_name":"atreides"}'
            ),
        )
