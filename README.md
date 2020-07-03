# ASGI from scratch

This repository implements an [ASGI](https://asgi.readthedocs.io/en/latest/index.html) compatible HTTP server from scratch as well as a companion ASGI application. No dependencies are needed as long as you're running Python 3.8. The idea behind this repository is to grok how ASGI works and what is the role of the ASGI protocol server and the ASGI application itself and how they communicate.

## How it works

The [ASGI specification](http://link-here) is rather short so I'd suggest reading through it if you're interested but what follows is a minimalistic summary of it. A typical ASGI application can essentially be split into two components:

* a protocol server
* an application

INSERT PICTURE HERE

The protocol server is responsible for decoding protocol data into ASGI specification compliant messages which are then sent to the application. The messages themselves are usually simple Python dictionaries. The application can also send ASGI specification compliant messages in the other direction, i.e. to the protocol server which then needs to encode those messages to conform to the protocol.

In the context of HTTP this means that the protocol server is more or less a TCP socket server which decodes the HTTP protocol into messages defined by the [ASGI specification for HTTP](http://link-here) which are then passed to the application. The application can also send HTTP responses as ASGI messages to the protocol server and the protocol server needs to encode those messages to match the HTTP protocol.

Note that each protocol has their own protocol specific ASGI specification. The main ASGI specification itself is concerned with this split between the protocol server and the application, not the specific messages defined for a common protocol. In this repository the HTTP protocol server is defined in the [server](http://link-here) module as well as the [http](http://link-here) module.

The ASGI applications called by the protocol server themselves are typically simple coroutines:

```python
async def application(scope, receive, send):
    ...
```

Scope is a dictionary containing relevant information for the current connection and / or request. In the context of HTTP the scope dictionary will contain things like the HTTP method and path but not the body of the HTTP request. `receive` is a coroutine which can be `await`ed for to retrieve the body of the HTTP request and `send` is a coroutine which can be used to send the HTTP response by calling it with ASGI compliant HTTP response messages.

And that's more or less it. Some details have obviously been omitted but to summarize the whole thing in a few short steps:

- a protocol server decodes protocol traffic into messages / dictionaries defined by the relevant protocol specification
- the application coroutine can consume those messages and send back messages of its own
- the protocol server will encode the messages sent by the application to conform to the protocol

## Limitations

Note that the HTTP server is very, very barebones and is only meant to serve as a teaching tool for understanding ASGI - nothing more. Nothing included in this repository is meant to be run in production. The HTTP request parsing is neither robust nor safe, the connection handling is inadequate and the protocol server probably does not fully implement the ASGI specication for HTTP.

## Usage

To run the protocol server:

```shell
python3 -m asgi.server
```

To run tests:

```shell
python3 -m unittest discover tests/
```