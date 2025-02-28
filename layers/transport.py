from collections.abc import Callable

import layer_log as log
from common import Ip4Addr


NAME = "transport"


type TransportReceiverFn = Callable[[Ip4Addr, bytes], None]
type TransportSenderFn = Callable[[Ip4Addr, bytes], None]


class TransportLayer:
    def __init__(self):
        pass

    def set_link(
        self,
        receiver: TransportReceiverFn,
        sender: TransportSenderFn,
    ):
        self.receiver = receiver
        self.sender = sender

    def receive(self, addr: Ip4Addr, data: bytes):
        pass

    def send(self, addr: Ip4Addr, data: bytes):
        pass
