"""ASGI example application"""


async def app(scope, receive, send):
    print(f"Received {scope}")
    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [[b"content-type", b"text/plain"]],
        }
    )
    await send({"type": "http.response.body", "body": b"Hi there"})
