from layers.physical import PhysicalLayer
from layers.data_link import DataLinkLayer


def main():
    physical = PhysicalLayer()
    data_link = DataLinkLayer(physical.make_commander())

    physical.listen(("127.0.0.1", 8080), data_link.receive)


if __name__ == "__main__":
    main()
