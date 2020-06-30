from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List

from asgi.exceptions import HttpRequestParsingException


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
            lines = raw.split("\r\n")
            method, path, protocol = lines[0].split()
            headers = HttpRequest._parse_headers(lines[1:])
            if "content-length" in headers:
                body = HttpRequest._parse_body(lines[-1])
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
            # FIXME: The body should not be passed to this function
            if not header.strip():
                break
            name = header[: header.find(":")].strip()
            value = header[header.find(":") + 1 :].strip()
            headers[name.lower()] = value

        return headers

    @staticmethod
    def _parse_body(body: str) -> str:
        """Parses body"""
        # TODO: Implement JSON parsing
        return body
