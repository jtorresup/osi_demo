import math
import random


type Bit = int
type Port = int


class Mac:
    def __init__(self, raw: bytes = None):
        self.raw = raw or random.randbytes(6)

    def __repr__(self) -> str:
        return self.raw.hex(":")


class Ip4Addr:
    def __init__(self):
        self.a = random.randint(0, 999)
        self.b = random.randint(0, 999)
        self.c = random.randint(0, 999)
        self.d = random.randint(0, 999)

    def __str__(self) -> str:
        return f"{self.a}.{self.b}.{self.c}.{self.d}"

    def __repr__(self) -> str:
        return str(self)

    def to_bytes(self) -> bytes:
        return (
            self.a.to_bytes()
            + self.b.to_bytes()
            + self.c.to_bytes()
            + self.d.to_bytes()
        )


def int_to_bytes(n: int, *args, **kwargs) -> bytes:
    bitlen = math.ceil(n.bit_length() / 8)

    return n.to_bytes(bitlen, *args, **kwargs)
