from packet import Packet
from layer_config import LayerConfig


class Layer:
    def __init__(self, config: LayerConfig, packet: Packet, size_total: int, size_payload: int) -> None:
        self.packet = packet
        self.size_total = size_total
        self.size_payload = size_payload
        self.layer_type = config.layer_type
        self.name = config.name
        self.data = config.data

    @property
    def time(self):
        return self.packet.time
    
    @property
    def up(self):
        return self.packet.layers[self.layer_type - 1] if self.layer_type > 0 else None
    
    @property
    def down(self):
        return self.packet.layers[self.layer_type + 1] if self.layer_type < len(self.packet.layers) - 1 else None
    
    def __str__(self) -> str:
        return f"name = {self.name}\n" + f"size_total = {self.size_total}\n" + f"size_payload = {self.size_payload}\n" + f"data = {self.data}\n"
    