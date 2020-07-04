"""Integration tests between the protocol server and ASGI applications"""
import unittest
import asyncio

from asgi import server
from fakes import StreamReader, StreamWriter


class TestProtocolServer(unittest.TestCase):
    """Tests protocol server against various ASGI applications"""

    def test_echo_http_method(self):
        """Tests echoing HTTP request method to HTTP response body"""

        async def app(scope, receive, send):
            await send(
                {
                    "type": "http.response.start",
                    "status": 200,
                    "headers": [[b"content-type", b"text/plain"],],
                }
            )
            await send(
                {
                    "type": "http.response.body",
                    "body": f"HTTP request method: {scope['method']}".encode("utf-8"),
                    "more_body": False,
                }
            )

        request = (
            b"GET /api/v1/ HTTP/1.0\r\n"
            b"User-Agent: curl/7.54.0\r\n"
            b"Host: localhost:8000\r\n"
            b"\r\n"
        )
        reader = StreamReader(request)
        writer = StreamWriter()
        handle_request = server.use_application(app)(reader, writer)
        asyncio.run(handle_request)
        self.assertEqual(
            writer.stream,
            b"HTTP/1.0 200 OK\r\n"
            b"content-type: text/plain\r\n"
            b"\r\n"
            b"HTTP request method: GET",
        )

    def test_echoing_request_body(self):
        """Tests echoing HTTP request body to HTTP response body"""

        async def app(scope, receive, send):
            body = await receive()
            await send(
                {
                    "type": "http.response.start",
                    "status": 200,
                    "headers": [[b"content-type", b"text/plain"],],
                }
            )
            await send(
                {
                    "type": "http.response.body",
                    "body": body["body"],
                    "more_body": False,
                }
            )

        request = (
            b"POST /api/v1/ HTTP/1.0\r\n"
            b"User-Agent: curl/7.54.0\r\n"
            b"Host: localhost:8000\r\n"
            b"Content-Length: 44\r\n"
            b"\r\n"
            b'{"first_name":"paul","last_name":"atreides"}'
        )
        reader = StreamReader(request)
        writer = StreamWriter()
        handle_request = server.use_application(app)(reader, writer)
        asyncio.run(handle_request)
        self.assertEqual(
            writer.stream,
            b"HTTP/1.0 200 OK\r\n"
            b"content-type: text/plain\r\n"
            b"\r\n"
            b'{"first_name":"paul","last_name":"atreides"}',
        )
