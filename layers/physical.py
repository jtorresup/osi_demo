from __future__ import annotations

import socket
from collections.abc import Callable
from typing import List, Optional, Tuple

import layer_log as log


MAX_RECIEVE = 1024
MAX_PORTS = 4


class PhysicalLayerCommander:
    def __init__(self, physical: PhysicalLayer):
        self.physical = physical

    def send_to_port(self, port_id: int, data: bytes, close=False):
        self.physical.conn.sendall(data)
        if close:
            self.physical.free_port(port_id)

    def free_port(self, port_id: int):
        self.physical.free_port(port_id)


class PhysicalLayer:
    def __init__(self):
        self.ports: List[Optional[socket.socket]] = [
            None for _ in range(MAX_PORTS)
        ]

    def make_commander(self) -> PhysicalLayerCommander:
        return PhysicalLayerCommander(self)

    def free_port(self, port_id: int):
        self.ports[port_id].close()
        self.ports[port_id] = None

    def allocate_port(self, conn: socket.sockset) -> Optional[int]:
        for nth, port in enumerate(self.ports):
            if port is None:
                self.ports[nth] = conn
                return nth

        return None

    def run(
        self,
        addr: Tuple[str, int],
        receive_handler: Callable[[int, bytes], None],
    ):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(addr)
            sock.listen(MAX_PORTS)
            log.info("physical", "listening at:", addr)

            while True:
                try:
                    conn, conn_addr = sock.accept()
                except KeyboardInterrupt:
                    break

                port_id = self.allocate_port(conn)
                if port_id is not None:
                    log.info(
                        "physical",
                        f"address {conn_addr} connected to port {port_id}",
                    )
                else:
                    log.warn("physical", "all ports in use")

                for port in self.ports:
                    if port is None:
                        continue
                    if data := port.recv(MAX_RECIEVE):
                        receive_handler(port_id, data)

            log.info("physical", "shutting down...")
