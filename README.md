# ASGI from scratch

This repository implements an [ASGI](https://asgi.readthedocs.io/en/latest/index.html) compatible HTTP server from scratch as well as a companion ASGI application. No dependencies are needed as long as you're running Python 3.8. The idea behind this repository is to grok how ASGI works and what is the role of the ASGI protocol server and the ASGI application itself and how they communicate.

## Limitations

Note that the HTTP server is very, very barebones and is only meant to serve as a teaching tool for understanding ASGI - nothing more. Nothing included in this repository is meant to be run in production. The HTTP request parsing is neither robust nor safe, the connection handling is inadequate and the protocol server does not fully implement the ASGI specication.

## Usage

To run the protocol server:

```shell
python3 -m asgi.server
```

To run tests:

```shell
python3 -m unittest discover tests/
```