from __future__ import annotations

import random
from typing import TypeVar


T = TypeVar("T")


type Bit = int
type PhysicalPort = int
type IpPort = int


class NotEnoughBytes(Exception):
    pass


class Mac:
    def __init__(self, raw: bytes = None):
        self.raw = raw or random.randbytes(6)

    def __repr__(self) -> str:
        return self.raw.hex(":")

    def __eq__(self, o: Mac) -> bool:
        return self.raw == o.raw

    def __hash__(self) -> int:
        return hash(self.raw)

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

    def __eq__(self, o: Ip4Addr) -> bool:
        return (
            self.a == o.a
            and self.b == o.b
            and self.c == o.c
            and self.d == o.d
        )

    def __hash__(self) -> int:
        return hash(self.to_bytes())

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


def calc_checksum(header: bytes) -> bytes:
    checksum = 0
    for ith in range(0, len(header) // 2, 2):
        checksum += int.from_bytes(header[ith:ith + 2])
    if checksum.bit_length() > 16:
        checksum += checksum >> 16

    return checksum.to_bytes(2)
