from layers.physical import PhysicalLayer
from layers.datalink import DataLinkLayer


def main():
    phys = PhysicalLayer()
    datalink = DataLinkLayer()

    phys.run(("127.0.0.1", 5432), datalink.receive)


if __name__ == "__main__":
    main()
