from array import array

import layer_log as log
from utils import Bit


MAX_FRAME_SIZE = 4  # in bytes


class DataLinkLayer:
    name = "datalink"
    framebuffer = array("B")

    def receive(self, bit: Bit):
        self.framebuffer.append(bit)
        if len(self.framebuffer) < MAX_FRAME_SIZE * 8:
            return

        frame = self.build_frame()
        log.info(self.name, "frame:", frame)

        self.framebuffer.clear()

    def build_frame(self) -> bytes:
        frame = b""

        self.framebuffer.reverse()  # little to big endian
        for nth in range(0, MAX_FRAME_SIZE * 8, 8):
            byte = self.framebuffer[nth:nth + 8]
            buff = 0
            for bit in byte:
                buff <<= 1
                buff += bit
            frame += buff.to_bytes()

        return frame
