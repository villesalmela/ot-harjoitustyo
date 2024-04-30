from typing import Any

from layers.layer_config import LayerConfig
from layers.layer_level import LayerLevel
from components.enum_property import EnumProperty


class CookedPacketType(EnumProperty):
    """Property of SLL layer, holding Cooked Packet Type.
    
    Will not raise ValueError if called with invalid value, returns None instead."""
    UNICAST = 0
    BROADCAST = 1
    MULTICAST = 2
    UNICAST_TO_ANOTHER_HOST = 3
    SENT_BY_US = 4

class SLL(LayerConfig):
    """Configuration for SLL layer.
    
    SLL (Linux cooked capture) is a link layer protocol used by Linux for packet capture.
    """

    layer_type = LayerLevel.LINK
    layer_name = "SLL"
    data: dict[str, Any]

    def __init__(self, src_addr: str, packet_type: CookedPacketType, protocol_type: str) -> None:
        """Initializes SLL configuration object with provided details.

        Args:
            src_addr (str): source address
            packet_type (CookedPacketType): packet type
            protocol_type (str): protocol type
        """

        self.data = {
            "src_addr": src_addr,
            "packet_type": packet_type,
            "protocol_type": protocol_type
        }
