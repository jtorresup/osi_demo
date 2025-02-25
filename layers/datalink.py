from __future__ import annotations

import random
from typing import Dict, List

import layer_log as log
from layers import physical
from layers.physical import MAX_PORTS, PhysicalLayerCommander


MAX_FRAME_LEN = physical.MAX_RECIEVE // 2


def generate_random_mac() -> bytes:
    return random.randbytes(6)


def get_mac_from_frame(frame: bytes) -> bytes:
    pass


class DataLinkLayer:
    def __init__(self, physcmd: PhysicalLayerCommander):
        self.physcmd = physcmd
        self.topology: Dict[int, List[bytes]] = {
            nth: [] for nth in range(MAX_PORTS)
        }

    def receive(self, port_id: int, data: bytes):
        log.info("data link", "received:", data)

        # 1. Frame the data.
        # 2. Get mac address in bytes.
        # 3. If it's in the same port, then continue.
        #    Else, check every mapped port if it is there.
        #    Otherwise, append the mac to the list of port_id.
        # 4. Send it up the OSI stack

        return False
