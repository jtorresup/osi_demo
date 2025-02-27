from layers.physical import PhysicalLayer
from layers.datalink import DataLinkLayer
from layers.network import NetworkLayer

import layer_log as log


def main():
    physical = PhysicalLayer()
    datalink = DataLinkLayer()
    network = NetworkLayer()

    datalink.set_link(network.receive, physical.send)
    physical.run(("127.0.0.1", 5432), datalink.receive)


if __name__ == "__main__":
    main()
