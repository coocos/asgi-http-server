"""CLI for HTTP server"""
import argparse


def parse_cli_arguments() -> argparse.Namespace:

    parser = argparse.ArgumentParser(description="ASGI HTTP server")
    parser.add_argument(
        "application", default="asgi.example:app", help="ASGI application",
    )
    parser.add_argument("--port", default=8000, type=int, help="port to bind to")
    return parser.parse_args()
