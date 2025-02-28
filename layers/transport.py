from __future__ import annotations

import random
from collections.abc import Callable
from enum import IntEnum
from typing import Dict

import layer_log as log
from common import calc_checksum, Ip4Addr, IpPort


NAME = "transport"

# tcp header flags
CWR = 0b1000_0000
ECE = 0b0100_0000
URG = 0b0010_0000
ACK = 0b0001_0000
PSH = 0b0000_1000
RST = 0b0000_0100
SYN = 0b0000_0010
FIN = 0b0000_0001


type TransportReceiverFn = Callable[[Ip4Addr, bytes], None]
type TransportSenderFn = Callable[[IpPort, bytes], None]


class ReceiveState(IntEnum):
    HANDSHAKE = 0
    DATA = 1
    TERMINATE = 2


class TcpSegment:
    def __init__(self, raw: bytes):
        self.raw = raw

    @property
    def source_port(self) -> IpPort:
        return IpPort.from_bytes(self.raw[0:2])

    @property
    def destination_port(self) -> IpPort:
        return IpPort.from_bytes(self.raw[2:4])

    @property
    def checksum(self) -> bytes:
        return self.raw[16:18]

    @property
    def seq(self) -> int:
        return int.from_bytes(self.raw[4:8])

    @property
    def ack(self) -> bytes:
        return int.from_bytes(self.raw[8:12])

    @property
    def offset(self) -> int:
        return self.raw[12] >> 4

    @property
    def data(self) -> bytes:
        return self.raw[self.offset:]

    @staticmethod
    def build_one(
        dst_port: IpPort,
        src_port: IpPort,
        seq: int,
        ack: int,
        flags: int,
        data: bytes,
    ) -> TcpSegment:
        DATA_OFFSET = 5
        header = (
            src_port.to_bytes()
            + dst_port.to_bytes()
            + seq.to_bytes(4)
            + ack.to_bytes(4)
            # data offset and reserved, no options
            + (DATA_OFFSET << 4).to_bytes(2)
            + flags.to_bytes()
            + random.randbytes(2)
            + b"\0\0"  # initial checksum, to be calculated later
            + random.randbytes(2)
        )
        header = (
            header[:(DATA_OFFSET * 32 // 8) - 4]
            + calc_checksum(header)
            + header[18:]
        )

        return TcpSegment(header + data)


class TransportLayer:
    def __init__(self):
        self.port_table: Dict[IpPort, Ip4Addr] = {}
        self.recv_state = ReceiveState
        self.segment_buffer = b""

    def set_link(
        self,
        receiver: TransportReceiverFn,
        sender: TransportSenderFn,
    ):
        self.receiver = receiver
        self.sender = sender

    def receive(self, addr: Ip4Addr, data: bytes):
        match self.recv_state:
            case ReceiveState.HANDSHAKE:
                pass
            case ReceiveState.DATA:
                pass
            case ReceiveState.TERMINATE:
                pass

    def send(self, addr: Ip4Addr, data: bytes):
        pass
