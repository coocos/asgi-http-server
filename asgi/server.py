"""ASGI protocol server for HTTP 1.1"""
import asyncio

from asgi.tools import HttpRequest


async def process_http_request(reader: asyncio.streams.StreamReader) -> HttpRequest:
    """
    Reads until a complete HTTP request can be parsed and returns the request
    """
    buf = bytearray()
    while not buf.endswith(b"\r\n\r\n"):
        data = await reader.read(64)
        buf += data
    return HttpRequest.from_raw_request(buf.decode("utf-8"))


# FIXME: Add type hints
async def handle_connection(
    reader: asyncio.streams.StreamReader, writer: asyncio.streams.StreamWriter
) -> None:

    # FIXME: This should read until the entire HTTP request has been consumed
    request = await process_http_request(reader)
    print(request)

    writer.write(b"Thanks")
    await writer.drain()
    writer.close()


async def serve():
    server = await asyncio.start_server(handle_connection, "127.0.0.1", 8000)

    async with server:
        await server.serve_forever()


asyncio.run(serve())
