from datetime import datetime


class Packet:

    def __init__(self, time: datetime, size: int) -> None:
        self.time = time
        self.size = size
        self.layers = {}

    def __str__(self) -> str:
        out = f"time = {self.time}\n" + f"size = {self.size}\n\n"
        for layer_type, layer in self.layers.items():
            out += f"{layer_type.name}\n"
            out += f"{layer}\n"

        return f"### PACKET START ###\n{out.strip()}\n### PACKET END ###\n"
