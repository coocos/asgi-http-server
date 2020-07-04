"""Common exceptions"""


class HttpRequestParsingException(ValueError):
    """Raised when parsing raw request to HttpRequest object fails"""


class UnknownAsgiMessageType(Exception):
    """Raised when protocol server receives an unknown ASGI message"""
