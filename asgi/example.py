"""ASGI example application"""


async def app(scope, receive, send):
    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [
                [b"content-type", b"application/json"],
                [b"content-length", b"44"],
            ],
        }
    )
    await send(
        {
            "type": "http.response.body",
            "body": b'{"first_name":"paul","last_name":"atreides"}',
            "more_body": False,
        }
    )
