import socket
from collections.abc import Callable
from typing import Tuple

import layer_log as log
from utils import Bit


type ReceiveFn = Callable[[Bit], None]


class PhysicalLayer:
    name = "physical"

    def run(self, addr: Tuple[str, int], handler: ReceiveFn):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(addr)
            sock.listen(1)
            log.info(self.name, "listening at:", addr)

            while True:
                try:
                    conn, conn_addr = sock.accept()
                    log.info(self.name, "connected:", conn_addr)
                    with conn:
                        self.handle_connection(conn, handler)
                except KeyboardInterrupt:
                    break

            log.info(self.name, "shutting down...")

    def handle_connection(self, conn: socket.socket, handler: ReceiveFn):
        while byte := conn.recv(1):
            # simulate bit streaming
            byte = int.from_bytes(byte)
            for _ in range(8):
                bit = byte & 1
                handler(bit)
                byte >>= 1
