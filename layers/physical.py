import socket
from collections.abc import Callable
from typing import Dict, Tuple

import layer_log as log
from common import Bit, PhysicalPort


NAME = "physical"


type PhysicalReceiverFn = Callable[[PhysicalPort, Bit], None]


class PhysicalLayer:
    port_table: Dict[PhysicalPort, socket.socket] = {}

    def run(self, addr: Tuple[str, int], receiver: PhysicalReceiverFn):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(addr)
            sock.listen(1)
            log.info(NAME, "listening at:", addr)

            while True:
                try:
                    conn, (_, port) = sock.accept()
                    with conn:
                        self.handle_connection(conn, port, receiver)
                except KeyboardInterrupt:
                    break

            log.info(NAME, "shutting down...")

    def handle_connection(
        self,
        conn: socket.socket,
        port: PhysicalPort,
        receiver: PhysicalReceiverFn,
    ):
        self.port_table[port] = conn
        log.info(NAME, "receiving bits from port", port)
        while byte := conn.recv(1):
            # simulate bit streaming
            byte = int.from_bytes(byte)
            for _ in range(8):
                bit = byte & 1
                receiver(port, bit)
                byte >>= 1

    def send(self, port: PhysicalPort, data: bytes):
        conn = self.port_table[port]
        try:
            conn.sendall(data)
        except ConnectionRefusedError:
            del self.port_table[port]
