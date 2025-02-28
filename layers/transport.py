from __future__ import annotations

import random
from collections.abc import Callable
from enum import IntEnum
from typing import Dict

import layer_log as log
from common import Ip4Addr, IpPort


NAME = "transport"


type TransportReceiverFn = Callable[[Ip4Addr, bytes], None]
type TransportSenderFn = Callable[[IpPort, bytes], None]


class ReceiveState(IntEnum):
    HANDSHAKE = 0
    DATA = 1
    TERMINATE = 2


class TcpSegment:
    def __init__(self, raw: bytes):
        self.raw = raw

    @staticmethod
    def build_one(
        dst_port: IpPort,
        src_port: IpPort,
        seq: int,
        ack: int,
        is_ack: bool,
        is_syn: bool,
        is_fin: bool,
        data: bytes,
    ) -> TcpSegment:
        header = (
            src_port.to_bytes()
            + dst_port.to_bytes()
            + seq.to_bytes(4)
            + ack.to_bytes(4)
            + b"\50"  # data offset and reserved, no options
            + (is_ack << 4) + (is_syn << 1) + is_fin
            + random.randbytes(2)
        )


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
        log.debug(NAME, data)
        match self.recv_state:
            case ReceiveState.HANDSHAKE:
                pass
            case ReceiveState.DATA:
                pass
            case ReceiveState.TERMINATE:
                pass

    def send(self, addr: Ip4Addr, data: bytes):
        pass
