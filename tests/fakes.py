"""Fakes used by tests"""


class StreamReader:
    """Fake implementation of asyncio.streams.StreamReader"""

    def __init__(self, stream: bytearray):
        self._stream = stream

    async def read(self, bytes_: int = 0) -> bytes:
        next_bytes = self._stream[:bytes_]
        self._stream = self._stream[bytes_:]
        return next_bytes


class StreamWriter:
    """Fake implementation of asyncio.streams.StreamWriter"""

    def __init__(self):
        self.stream = bytearray()
        self.closed = False

    def write(self, data: bytes) -> None:
        self.stream += data

    def close(self) -> None:
        self.closed = True

    async def drain(self) -> None:
        pass

    async def wait_closed(self) -> None:
        pass
