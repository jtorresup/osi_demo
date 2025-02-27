from __future__ import annotations

import random
from collections.abc import Callable
from typing import Dict

import layer_log as log
from common import Ip4Addr, Mac


NAME = "network"


type NetworkReceiverFn = Callable[[Ip4Addr, bytes], None]
type NetworkSenderFn = Callable[[Mac, bytes], None]


class Ip4Packet:
    def __init__(self, inner: bytes):
        self.inner = inner

    @property
    def header(self) -> bytes:
        pass

    @property
    def data(self) -> bytes:
        pass

    @staticmethod
    def build(dst_ip: Ip4Addr, src_ip: Ip4Addr, data: bytes) -> Ip4Packet:
        version_and_ihl = (4 << 4) + 16
        dscp_and_ecn = 0
        total_length = len(data) + 16
        id = random.randbytes(2)

    def to_bytes(self) -> bytes:
        return self.inner


class NetworkLayer:
    def __init__(self):
        self.ip_table: Dict[Ip4Addr, Mac] = {}
        self.ip_rev_table: Dict[Mac, Ip4Addr] = {}
        self.ip = Ip4Addr()
        log.info(NAME, "generated ip:", self.ip)

    def set_link(self, receiver: NetworkReceiverFn, sender: NetworkSenderFn):
        self.receiver = receiver
        self.sender = sender

    def receive(self, src_mac: Mac, data: bytes):
        ip = self.get_ip_address(src_mac)
        dg = Ip4Packet(data)

    def send(self, ip: Ip4Addr, data: bytes):
        mac = self.ip_table[ip]
        datagram = Ip4Packet.build(ip, self.ip, data).to_bytes()
        log.info(NAME, "sending datagram:", datagram)
        self.sender(mac, datagram)

    def get_ip_address(self, mac: Mac) -> Ip4Addr:
        ip = self.ip_rev_table.get(mac, None)
        if ip is None:
            ip = Ip4Addr()
            self.ip_table[ip] = mac
            self.ip_rev_table[mac] = ip

        return ip
