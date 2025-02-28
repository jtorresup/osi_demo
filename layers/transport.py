from common import Ip4Addr


class TransportLayer:
    def receive(self, addr: Ip4Addr, data: bytes):
        pass

    def send(self, addr: Ip4Addr, data: bytes):
        pass
