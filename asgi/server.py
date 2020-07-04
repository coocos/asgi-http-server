"""ASGI protocol server for HTTP 1.0"""
import asyncio
from dataclasses import dataclass, field
from typing import Optional, Dict

from dataclasses import dataclass
from asgi.http import HttpResponse, AsgiHttpRequest, AsgiHttpResponse
from asgi.example import app
from asgi import exceptions


async def handle_request(
    reader: asyncio.streams.StreamReader, writer: asyncio.streams.StreamWriter
) -> None:
    """Handles a single HTTP request-response pair"""

    request = AsgiHttpRequest(reader)
    response = AsgiHttpResponse(writer)
    scope = await request.scope()
    # FIXME: You should be able to pass the application here so that you can mock it in tests etc
    await app(scope, request.read, response.write)
    await response.send()


async def serve() -> None:
    """Starts HTTP server"""
    server = await asyncio.start_server(handle_request, "127.0.0.1", 8000)

    async with server:
        await server.serve_forever()


if __name__ == "__main__":

    asyncio.run(serve())
