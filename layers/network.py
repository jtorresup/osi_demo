from __future__ import annotations

import math
import random
from collections.abc import Callable
from enum import IntEnum
from typing import Dict, List

import layer_log as log
from common import chunks, Ip4Addr, Mac


NAME = "network"


type NetworkReceiverFn = Callable[[Ip4Addr, bytes], None]
type NetworkSenderFn = Callable[[Mac, bytes], None]


class ReceiveState(IntEnum):
    HEADER = 0
    DATA = 1


class Ip4Packet:
    VERSION = 4
    MAX_DATA_SIZE = 65475  # in bytes
    HEADER_LENGTH = 5  # in 32-bit words, min length, no options

    def __init__(self, inner: bytes):
        self.inner = inner

    @property
    def source_address(self) -> Ip4Addr:
        return Ip4Addr.from_bytes(self.inner[12:16])

    @property
    def destination_address(self) -> Ip4Addr:
        return Ip4Addr.from_bytes(self.inner[16:20])

    @property
    def data(self) -> bytes:
        return self.inner[self.HEADER_LENGTH:]

    @staticmethod
    def build_all(
        dst_ip: Ip4Addr,
        src_ip: Ip4Addr,
        data: bytes,
    ) -> List[Ip4Packet]:
        packet_count = math.ceil(len(data) / Ip4Packet.MAX_DATA_SIZE)
        packets = []

        for packet_data in chunks(data, packet_count):
            packet = Ip4Packet.build_one(dst_ip, src_ip, packet_data)
            packets.append(packet)

        return packets

    @staticmethod
    def build_one(dst_ip: Ip4Addr, src_ip: Ip4Addr, data: bytes) -> Ip4Packet:
        version_and_ihl = (
            (Ip4Packet.VERSION << 4) + Ip4Packet.HEADER_LENGTH
        ).to_bytes()
        dscp_and_ecn = b"\0"  # not real time and demo world has no congestion
        total_length = (len(data) + Ip4Packet.HEADER_LENGTH).to_btyes(2)
        id = random.randbytes(2)
        flags_and_frag_offset = (2 << 13).to_bytes(2)  # no fragmentation
        ttl = random.randbytes(1)
        protocol = (6).to_bytes()  # always tcp in demo

        header = (
            version_and_ihl
            + dscp_and_ecn
            + total_length
            + id
            + flags_and_frag_offset
            + ttl
            + protocol
            + b"\0\0"  # checksum at 0 so we can calc it later
            + src_ip.to_bytes()
            + dst_ip.to_bytes()
        )
        checksum = Ip4Packet.calc_checksum(header)
        header = (
            header[:(Ip4Packet.HEADER_LENGTH * 32 // 8) - 8]
            + checksum
            + src_ip.to_bytes()
            + dst_ip.to_bytes()
        )

        return Ip4Packet(header + data)

    @staticmethod
    def calc_checksum(header: bytes) -> bytes:
        chk = 0
        for left, right in chunks(header, 2):
            chk += ((left << 8) + right) ^ 0xffff

        return (chk ^ 0xffff).to_bytes()

    def to_bytes(self) -> bytes:
        return self.inner


class NetworkLayer:
    def __init__(self):
        self.ip = Ip4Addr()
        self.packet_buffer = b""
        self.ip_table: Dict[Ip4Addr, Mac] = {}
        self.recv_state = ReceiveState.HEADER
        log.info(NAME, "generated ip:", self.ip)

    def set_link(self, receiver: NetworkReceiverFn, sender: NetworkSenderFn):
        self.receiver = receiver
        self.sender = sender

    def receive(self, src_mac: Mac, data: bytes):
        self.packet_buffer += data

        match self.recv_state:
            case ReceiveState.HEADER:
                header_length = (self.packet_buffer[0] << 4) >> 4
                log.info(NAME, "header has size:", self.packet_size)
                if len(data) < (header_length * 32 // 8):
                    return

                self.packet_size = int.from_bytes(self.packet_buffer[2:4])
                self.recv_state = ReceiveState.DATA
                log.info(NAME, "packet has size:", self.packet_size)

            case ReceiveState.DATA:
                packet = Ip4Packet(self.packet_buffer[:self.packet_size])
                log.info(NAME, "packet from:", packet.source_address)
                log.info(NAME, "packet:", packet)

                self.recv_state = ReceiveState.HEADER
                self.ip_table[packet.source_address] = src_mac
                self.packet_buffer = self.packet_buffer[self.packet_size:]
                self.receiver(packet.source_address, packet.data)

    def send(self, ip: Ip4Addr, data: bytes):
        mac = self.ip_table[ip]
        packets = Ip4Packet.build_all(ip, self.ip, data)

        for packet in packets:
            log.info(NAME, "sending datagram:", packet)
            self.sender(mac, packet.to_bytes())
