from layers.physical import PhysicalLayer
from layers.datalink import DataLinkLayer


def main():
    physical = PhysicalLayer()
    datalink = DataLinkLayer(physical.make_commander())

    physical.run(("127.0.0.1", 8080), datalink.receive)


if __name__ == "__main__":
    main()
