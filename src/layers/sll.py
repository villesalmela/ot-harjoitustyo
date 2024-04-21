from layers.layer_config import LayerConfig
from layers.layer_level import LayerLevel
from layers.properties.cooked_packet_type import CookedPacketType


class SLL(LayerConfig):
    def __init__(self, src_addr: str, packet_type: CookedPacketType, protocol_type: str) -> None:

        super().__init__(LayerLevel.LINK, "SLL", {
            "src_addr": src_addr,
            "packet_type": packet_type,
            "protocol_type": protocol_type
        })
