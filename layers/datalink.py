from __future__ import annotations

import math
from array import array
from collections.abc import Callable
from typing import Dict, List

import layer_log as log
from common import Bit, Mac, NotEnoughBytes, Port


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
    def from_buffer(framebuffer: array) -> Frame:
        if len(framebuffer) < Frame.MAX_BYTE_SIZE * 8:
            raise NotEnoughBytes()

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
    def build_all(dst_mac: bytes, src_mac: bytes, data: bytes) -> List[Frame]:
        frames = []

        frame_count = math.ceil(len(data) / Frame.MAX_BODY_SIZE)
        for ith in range(frame_count):
            ith = ith * Frame.MAX_BODY_SIZE
            inner = data[ith:ith + Frame.MAX_BODY_SIZE]
            log.debug(NAME, ith, ith + Frame.MAX_BODY_SIZE, len(inner))
            padding = Frame.MAX_BODY_SIZE - len(inner)
            inner = inner + (b"\0" * padding)
            frames.append(Frame(dst_mac + src_mac + inner))

        return frames

    def to_bytes(self) -> bytes:
        return self.inner


class DataLinkLayer:
    def __init__(self):
        self.mac = Mac()
        self.framebuffer = array("B")
        self.mac_table: Dict[Mac, Port] = {}
        log.info(NAME, "generated mac:", self.mac)

    def set_link(self, receiver: DataLinkReceiverFn, sender: DataLinkSenderFn):
        self.receiver = receiver
        self.sender = sender

    def receive(self, port: Port, bit: Bit):
        self.framebuffer.append(bit)

        try:
            frame = Frame.from_buffer(self.framebuffer)
        except NotEnoughBytes:
            return

        self.framebuffer.clear()
        log.info(NAME, "from mac:", frame.source_mac)
        log.info(NAME, "frame:", frame)

        self.mac_table[frame.source_mac] = port
        self.receiver(frame.source_mac, frame.body)

    def send(self, mac: Mac, data: bytes):
        port = self.mac_table[mac]
        frames = Frame.build_all(mac, self.mac, data)

        for frame in frames:
            log.info(NAME, "sending frame:", frame.inner)
            self.sender(port, frame.inner)
