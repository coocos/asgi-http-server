"""ASGI interface handlers for HTTP requests and responses"""
import asyncio
from dataclasses import dataclass, field
from typing import Dict

from asgi.http import HttpRequest, HttpResponse
from asgi import exceptions


@dataclass
class AsgiHttpRequest:
    """Converts input stream to ASGI compliant HTTP request messages"""

    reader: asyncio.streams.StreamReader
    buffer: bytearray = field(default_factory=bytearray)

    async def scope(self) -> Dict:
        """Returns ASGI scope"""
        # Read until all headers have been read
        while not b"\r\n\r\n" in self.buffer:
            self.buffer += await self.reader.read(64)
        request = HttpRequest.deserialize(self.buffer)
        return {
            "type": "http",
            "asgi": {"version": "3.0", "spec_version": "2.0",},
            "http_version": "1.0",
            "method": request.method,
            "scheme": "http",
            "path": request.path,
            # FIXME: Implement query string parsing
            "query_string": "",
            "headers": [
                [header.encode("utf-8"), value.encode("utf-8")]
                for header, value in request.headers.items()
            ],
        }

    async def read(self) -> Dict:
        """Returns ASGI message with HTTP request contents"""
        # Read body if it's present
        request = HttpRequest.deserialize(self.buffer)
        if "content-length" in request.headers:
            body_start = self.buffer.find(b"\r\n\r\n") + 4
            while len(self.buffer[body_start:]) < int(
                request.headers["content-length"]
            ):
                self.buffer += await self.reader.read(64)
        request = HttpRequest.deserialize(self.buffer)
        return {"type": "http.request", "body": request.body, "more_body": False}


@dataclass
class AsgiHttpResponse:
    """Converts ASGI compliant HTTP messages to an output stream"""

    writer: asyncio.streams.StreamWriter

    async def write(self, message: Dict) -> None:
        """Writes HTTP response content to the active socket"""
        if message["type"] == "http.response.start":
            headers = {
                header.decode("utf-8"): value.decode("utf")
                for header, value in message["headers"]
            }
            response = HttpResponse(message["status"], headers)
            self.writer.write(response.serialize())
            await self.writer.drain()
        elif message["type"] == "http.response.body":
            # TODO: more_body needs to be handled for streaming writes
            self.writer.write(message["body"])
        else:
            raise exceptions.UnknownAsgiMessageType(
                f"{message['type']} is not a known message type"
            )

    async def send(self) -> None:
        """
        Finishes response by waiting until the buffer is drained
        and closes the connection
        """
        await self.writer.drain()
        self.writer.close()
        await self.writer.wait_closed()
