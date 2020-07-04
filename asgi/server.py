"""ASGI protocol server for HTTP 1.0"""
import asyncio
import importlib

from asgi.http import AsgiHttpRequest, AsgiHttpResponse
from asgi import cli


def use_application(app):
    """Uses passed ASGI application to handle HTTP requests"""

    async def handle_request(
        reader: asyncio.streams.StreamReader, writer: asyncio.streams.StreamWriter
    ) -> None:
        """Handles a single HTTP request-response pair"""

        request = AsgiHttpRequest(reader)
        response = AsgiHttpResponse(writer)
        scope = await request.scope()
        await app(scope, request.read, response.write)
        await response.send()

    return handle_request


def import_application(path: str):
    """Imports ASGI application coroutine and returns it"""
    module_path, app_name = path.split(":")
    module = importlib.import_module(module_path)
    return getattr(module, app_name)


async def serve() -> None:
    """Starts HTTP server"""
    args = cli.parse_cli_arguments()
    app = import_application(args.application)
    server = await asyncio.start_server(use_application(app), "127.0.0.1", args.port)

    async with server:
        await server.serve_forever()


if __name__ == "__main__":

    asyncio.run(serve())
