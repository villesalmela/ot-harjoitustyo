from datetime import datetime
from typing import Self
from uuid import uuid4

from utils.utils import flatten_dict


class Packet:
    """Stores a single network packet, containing all its different layers."""

    def __init__(self, time: datetime, size: int, packet_number: int) -> None:
        self.packet_uid = uuid4()
        self.time = time
        self.size = size
        self.layers = {}
        self.packet_number = packet_number

    def flatten(self) -> dict:
        """Flatten the packet into dictionary with max depth 1.

        Nested keys will merged into one, separated with dots.
        LayerLevel will be used as a key for each layer.

        For example source IP address on network layer will be assigned a key:
        NETWORK.IP.data.src_addr

        Returns:
            dict: flattened packet
        """
        d = {
            "packet.uid": self.packet_uid,
            "packet.time": self.time,
            "packet.size": self.size,
        }
        for layer_type, layer in self.layers.items():
            contents = layer.__dict__.copy()
            contents[f"{layer.layer_name}.data"] = contents["data"]
            del contents["data"]
            d.update({f"{layer_type}": contents})
        return flatten_dict(d)

    def __str__(self) -> str:
        """Get the string representation of this packet.

        Returns:
            str: details of the packet and all its layers.
        """
        out = f"number = {self.packet_number}\n" + \
            f"time = {self.time}\n" + f"size = {self.size}\n\n"
        for layer_type, layer in self.layers.items():
            out += f"{layer_type}\n"
            out += f"{layer}\n"

        return f"### PACKET START ###\n{out.strip()}\n### PACKET END ###\n"

    def __eq__(self, value: Self) -> bool:
        """Check if a packet equals another packet.

        Args:
            value (Self): The other packet

        Returns:
            bool: True if packets are equal, False otherwise.
        """
        if not isinstance(value, Packet):
            return False
        return self.time == value.time and \
            self.size == value.size and \
            self.layers == value.layers
