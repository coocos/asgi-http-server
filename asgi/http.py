from __future__ import annotations
import asyncio
from dataclasses import dataclass, field
from typing import Dict, List

from asgi import exceptions


STATUS_CODES = {200: "OK", 400: "Bad Request", 500: "Internal Server Error"}


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
        request = HttpRequest.deserialize(self.buffer.decode("utf-8"))
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
        request = HttpRequest.deserialize(self.buffer.decode("utf-8"))
        if "content-length" in request.headers:
            body_start = self.buffer.find(b"\r\n\r\n") + 4
            while len(self.buffer[body_start:]) < int(
                request.headers["content-length"]
            ):
                self.buffer += await self.reader.read(64)
        request = HttpRequest.deserialize(self.buffer.decode("utf-8"))
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
            print("Response body not implemented yet")
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


@dataclass
class HttpRequest:
    """HTTP request object"""

    # FIXME: Use enum or type this better
    method: str
    # FIXME: Create a proper URL object?
    path: str
    headers: Dict[str, str]
    body: str = ""

    @classmethod
    def deserialize(cls, raw: str) -> HttpRequest:
        """Constructs HttpRequest from string containing an entire HTTP request"""
        try:
            raw_headers, raw_body = raw.split("\r\n\r\n")
            header_lines = raw_headers.split("\r\n")
            method, path, protocol = header_lines[0].split()
            headers = HttpRequest._parse_headers(header_lines[1:])
            if "content-length" in headers:
                body = HttpRequest._parse_body(raw_body)
            else:
                body = ""
            return HttpRequest(method, path, headers, body)
        except Exception as err:
            raise exceptions.HttpRequestParsingException(f"Failed to parse {raw}")

    @staticmethod
    def _parse_headers(raw_headers: List[str]) -> Dict[str, str]:
        """Parses headers to a dictionary from a list of strings"""
        headers: Dict[str, str] = {}
        for header in raw_headers:
            name = header[: header.find(":")].strip()
            value = header[header.find(":") + 1 :].strip()
            headers[name.lower()] = value

        return headers

    @staticmethod
    def _parse_body(body: str) -> str:
        """Parses body"""
        # TODO: Implement JSON parsing
        return body


@dataclass
class HttpResponse:
    """HTTP response object"""

    status: int = 200
    headers: Dict[str, str] = field(default_factory=dict)

    def serialize(self) -> bytes:
        """Returns HTTP response as raw bytes"""
        headers = "\r\n".join(
            f"{header}: {value}" for header, value in self.headers.items()
        )
        return (
            f"HTTP/1.0 {self.status} {STATUS_CODES[self.status]}\r\n"
            f"{headers}\r\n"
            "\r\n"
        ).encode("utf-8")
