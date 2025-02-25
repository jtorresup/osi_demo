from layers import layer_log as log
from layers.physical import PhysicalLayerCommander


class DataLinkLayer:
    def __init__(self, physical_cmd: PhysicalLayerCommander):
        self.physical_cmd = physical_cmd
        self.buffer = b""

    def receive(self, data: bytes) -> bool:
        self.buffer += data
        log.info("data link", "currently buffered:", self.buffer)
        self.physical_cmd.close()

        return True
