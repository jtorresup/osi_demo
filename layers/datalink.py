from __future__ import annotations

from array import array
from collections.abc import Callable
from typing import Dict

import layer_log as log
from common import Bit, Mac, Port


NAME = "datalink"


type DataLinkReceiverFn = Callable[[Mac, bytes], None]
type DataLinkSenderFn = Callable[[Port, bytes], None]


class Frame:
    """
    Frame format:
        dst_mac:6 + src_mac:6 + pad_len:1 + body:255

        Legend:
            [name]:[byte_size]
    """
    MAX_BYTE_SIZE = 268  # in bytes
    MAX_BODY_SIZE = 255  # in bytes

    class NotEnoughBytes(Exception):
        pass

    def __init__(self, inner: bytes):
        self.inner = inner

    def __repr__(self) -> str:
        return f"<Frame : {self.inner}>"

    @property
    def source_mac(self) -> Mac:
        return Mac(self.inner[6:12])

    @property
    def destination_mac(self) -> Mac:
        return Mac(self.inner[:6])

    @property
    def padding(self) -> int:
        return self.inner[12]

    @property
    def body(self) -> bytes:
        return self.inner[13:len(self.inner) - self.padding]

    @staticmethod
    def from_framebuffer(framebuffer: array) -> Frame:
        if len(framebuffer) < Frame.MAX_BYTE_SIZE * 8:
            raise Frame.NotEnoughBytes()

        frame = b""
        framebuffer.reverse()
        for nth in range(0, Frame.MAX_BYTE_SIZE * 8, 8):
            byte = framebuffer[nth:nth + 8]
            buff = 0
            for bit in byte:
                buff <<= 1
                buff += bit
            frame = buff.to_bytes() + frame  # little to big endian

        return Frame(frame)

    @staticmethod
    def build(dst_mac: bytes, src_mac: bytes, data: bytes) -> Frame:
        padding = Frame.MAX_BODY_SIZE - len(data)
        data = data + (b"\0" * padding)

        return Frame(dst_mac + src_mac + data + padding)

    def to_bytes(self) -> bytes:
        return self.inner


class DataLinkLayer:
    def __init__(self):
        self.mac = Mac()
        self.recv_framebuffer = array("B")
        self.mac_table: Dict[Mac, Port] = {}
        log.info(NAME, "generated mac:", self.mac)

    def set_link(self, receiver: DataLinkReceiverFn, sender: DataLinkSenderFn):
        self.receiver = receiver
        self.sender = sender

    def receive(self, port: Port, bit: Bit):
        self.recv_framebuffer.append(bit)

        try:
            frame = Frame.from_framebuffer(self.recv_framebuffer)
        except Frame.NotEnoughBytes:
            return

        self.recv_framebuffer.clear()
        log.info(NAME, "from mac:", frame.source_mac)
        log.info(NAME, "frame:", frame)

        self.mac_table[frame.source_mac] = port
        self.receiver(frame.source_mac, frame.body)

    def send(self, mac: Mac, data: bytes):
        port = self.mac_table[mac]
        framedata = Frame.build(mac, self.mac, data).to_bytes()
        log.info(NAME, "sending frame:", framedata)
        self.sender(port, framedata)
