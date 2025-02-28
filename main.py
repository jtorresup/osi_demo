from collections.abc import Callable
from typing import Any

from layers.physical import PhysicalLayer
from layers.datalink import DataLinkLayer
from layers.network import NetworkLayer
from layers.transport import TransportLayer

import layer_log as log


def make_debug_layer(name: str) -> Callable[[Any, Any], None]:
    return lambda x, y: log.debug(name, x, y)


def main():
    transport = TransportLayer()
    network = NetworkLayer()
    datalink = DataLinkLayer()
    physical = PhysicalLayer()

    transport.set_link(make_debug_layer("session"), network.send)
    network.set_link(transport.receive, datalink.send)
    datalink.set_link(network.receive, physical.send)
    physical.run(("127.0.0.1", 5432), datalink.receive)


if __name__ == "__main__":
    main()
