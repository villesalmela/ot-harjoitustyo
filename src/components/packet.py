from datetime import datetime
from typing import Self
from uuid import uuid4

from components.layer import Layer


class Packet:

    def __init__(self, time: datetime, size: int, packet_number: int) -> None:
        self.packet_uid = uuid4()
        self.time = time
        self.size = size
        self.layers = {}
        self.packet_number = packet_number

    def add_layer(self, layer: Layer) -> None:
        layer.packet_uid = self.packet_uid
        self.layers[layer.layer_type] = layer

    def __str__(self) -> str:
        out = f"number = {self.packet_number}\n" + \
            f"time = {self.time}\n" + f"size = {self.size}\n\n"
        for layer_type, layer in self.layers.items():
            out += f"{layer_type.name}\n"
            out += f"{layer}\n"

        return f"### PACKET START ###\n{out.strip()}\n### PACKET END ###\n"

    def __eq__(self, value: Self) -> bool:
        if not isinstance(value, Packet):
            return False
        return self.time == value.time and \
            self.size == value.size and \
            self.layers == value.layers
