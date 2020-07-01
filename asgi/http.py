from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List

from asgi.exceptions import HttpRequestParsingException


STATUS_CODES = {200: "OK", 400: "Bad Request", 500: "Internal Server Error"}


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
    def from_raw_request(cls, raw: str) -> HttpRequest:
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
            raise HttpRequestParsingException(f"Failed to parse {raw}")

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

    def encode(self) -> bytes:
        """Returns HTTP response as raw bytes"""
        headers = "\r\n".join(
            f"{header}: {value}" for header, value in self.headers.items()
        )
        return (
            f"HTTP/1.0 {self.status} {STATUS_CODES[self.status]}\r\n"
            f"{headers}\r\n"
            "\r\n"
        ).encode("utf-8")
