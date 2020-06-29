from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class HttpRequest:
    """HTTP request object"""

    # FIXME: Use enum or type this better
    method: str
    # FIXME: Or create a proper URL object?
    path: str
    headers: Dict[str, str]

    @classmethod
    def from_raw_request(cls, raw: str) -> HttpRequest:
        """Constructs HttpRequest from string containing an entire HTTP request"""

        lines = raw.split("\r\n")
        method, path, protocol = lines[0].split()
        headers = HttpRequest._parse_headers(lines[1:])
        return HttpRequest(method, path, headers)

    @staticmethod
    def _parse_headers(raw_headers: List[str]) -> Dict[str, str]:
        """Parses headers to a dictionary from a list of strings"""
        headers: Dict[str, str] = {}
        for header in raw_headers:
            if header.strip():
                name, value = [part.strip() for part in header.split(":")]
                headers[name.lower()] = value
        return headers
