from layers.physical import PhysicalLayer
from layers.datalink import DataLinkLayer
from layers.network import NetworkLayer
from layers.transport import TransportLayer

import layer_log as log


def main():
    transport = TransportLayer()
    network = NetworkLayer()
    datalink = DataLinkLayer()
    physical = PhysicalLayer()

    network.set_link(transport.receive, datalink.send)
    datalink.set_link(network.receive, physical.send)
    physical.run(("127.0.0.1", 5432), datalink.receive)


if __name__ == "__main__":
    main()
