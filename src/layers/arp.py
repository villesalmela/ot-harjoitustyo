from layers.layer_config import LayerConfig
from layers.layer_level import LayerLevel
from layers.properties.arp_opcode import ARPOpCode
from layers.properties.hardware_type import HardwareType


class ARP(LayerConfig):
    def __init__(
            self,
            hwtype: HardwareType,
            opcode: ARPOpCode,
            hwsrc: str,
            hwdst: str,
            psrc: str,
            pdst: str) -> None:

        super().__init__(LayerLevel.LINK, "ARP", {
            "hwtype": hwtype,
            "opcode": opcode,
            "hwsrc": hwsrc,
            "hwdst": hwdst,
            "psrc": psrc,
            "pdst": pdst
        })
