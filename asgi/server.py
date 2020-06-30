"""ASGI protocol server for HTTP 1.1"""
import asyncio

from asgi.http import HttpRequest, HttpResponse


async def read_http_request(reader: asyncio.streams.StreamReader) -> HttpRequest:
    """
    Reads from connection until a complete HTTP request can be parsed and returns the request
    """
    buf = bytearray()
    # Read until all headers have been read
    while not b"\r\n\r\n" in buf:
        buf += await reader.read(64)
    request = HttpRequest.from_raw_request(buf.decode("utf-8"))

    # Read body if it's present
    if "content-length" in request.headers:
        body_start = buf.find(b"\r\n\r\n") + 4
        while len(buf[body_start:]) < int(request.headers["content-length"]):
            buf += await reader.read(64)
        # FIXME: Constructing the request twice is nasty - refactor reading the body
        request = HttpRequest.from_raw_request(buf.decode("utf-8"))

    return request


async def handle_connection(
    reader: asyncio.streams.StreamReader, writer: asyncio.streams.StreamWriter
) -> None:

    request = await read_http_request(reader)
    print(request)

    response = HttpResponse()
    writer.write(response.encode())
    await writer.drain()
    writer.close()


if __name__ == "__main__":

    async def serve():
        server = await asyncio.start_server(handle_connection, "127.0.0.1", 8000)

        async with server:
            await server.serve_forever()

    asyncio.run(serve())
