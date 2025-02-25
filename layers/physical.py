from __future__ import annotations

import socket
from typing import Callable, Tuple

from layers import layer_log as log


class PhysicalLayerCommander:
    def __init__(self, physical: PhysicalLayer):
        self.physical = physical

    def send(self, data: bytes, close=False):
        self.physical.conn.sendall(data)
        if close:
            self.physical.close_connection()

    def close(self):
        self.physical.close_connection()


class PhysicalLayer:
    def make_commander(self) -> PhysicalLayerCommander:
        return PhysicalLayerCommander(self)

    def close_connection(self):
        self.connected = False
        self.conn.close()

    def listen(
        self,
        addr: Tuple[str, int],
        receive: Callable[[bytes], bool],
    ):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(addr)
            sock.listen(1)
            log.info("physical", "listening at:", addr)
            while True:
                try:
                    conn, conn_addr = sock.accept()
                except KeyboardInterrupt:
                    log.info("physical", "shutting down...")
                    break

                self.conn = conn
                with conn:
                    log.info("physical", "connected with:", conn_addr)
                    self.connected = True
                    while self.connected:
                        if data := conn.recv(1024):
                            receive(data)
                    log.info("physical", "closing:", conn_addr)
