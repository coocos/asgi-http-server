"""ASGI example application"""


async def app(scope, receive, send):
    """Example application which servers a simple HTML page"""
    html = b"""
    <!doctype html>
    <html>
            <head>
                    <title>Hello ASGI!</title>
            </head>
            <body>
                    <main>
                    <h1>Hello ASGI!</h1>
                    </main>
            </body>
    </html>
    """
    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [[b"content-type", b"text/html"], [b"content-length", b"269"],],
        }
    )
    await send(
        {"type": "http.response.body", "body": html, "more_body": False,}
    )
