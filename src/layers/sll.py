from typing import Any

from layers.layer_config import LayerConfig
from layers.layer_level import LayerLevel
from components.enum_property import EnumProperty


class CookedPacketType(EnumProperty):
    UNKNOWN = None
    UNICAST = 0
    BROADCAST = 1
    MULTICAST = 2
    UNICAST_TO_ANOTHER_HOST = 3
    SENT_BY_US = 4


class SLL(LayerConfig):

    layer_type = LayerLevel.LINK
    layer_name = "SLL"
    data: dict[str, Any]

    def __init__(self, src_addr: str, packet_type: CookedPacketType, protocol_type: str) -> None:

        self.data = {
            "src_addr": src_addr,
            "packet_type": packet_type,
            "protocol_type": protocol_type
        }
