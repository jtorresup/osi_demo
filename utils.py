import math


type Bit = int


def int_to_bytes(n: int, *args, **kwargs) -> bytes:
    bitlen = math.ceil(n.bit_length() / 8)

    return n.to_bytes(bitlen, *args, **kwargs)
