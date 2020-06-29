from __future__ import annotations
from dataclasses import dataclass


@dataclass
class HttpRequest:
    """HTTP request object"""

    # FIXME: Use enum or type this better
    method: str
    # FIXME: Or create a proper URL object?
    path: str

    @classmethod
    def from_raw_request(cls, raw: str) -> HttpRequest:
        """Constructs HttpRequest from string containing an entire HTTP request"""
        lines = raw.split("\r\n")
        method, path, protocol = lines[0].split()
        return HttpRequest(method, path)
