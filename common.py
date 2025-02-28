from __future__ import annotations

import math
import random
from itertools import zip_longest
from typing import Iterable, Iterator, TypeVar


T = TypeVar("T")


type Bit = int
type Port = int


class NotEnoughBytes(Exception):
    pass


class Mac:
    def __init__(self, raw: bytes = None):
        self.raw = raw or random.randbytes(6)

    def __repr__(self) -> str:
        return self.raw.hex(":")

    def to_bytes(self) -> bytes:
        return self.raw


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

    @staticmethod
    def from_bytes(raw: bytes) -> Ip4Addr:
        addr = Ip4Addr()
        addr.a = raw[0]
        addr.b = raw[1]
        addr.c = raw[2]
        addr.d = raw[3]

        return addr


def int_to_bytes(n: int, *args, **kwargs) -> bytes:
    bitlen = math.ceil(n.bit_length() / 8)

    return n.to_bytes(bitlen, *args, **kwargs)


def chunks(iterable: Iterable[T], n: int) -> Iterator[T]:
    iters = [iter(iterable)] * n

    return zip_longest(*iters)
