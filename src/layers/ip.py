from typing import Any

from layers.layer_config import LayerConfig
from layers.layer_level import LayerLevel
from components.enum_property import EnumProperty


class IPVersion(EnumProperty):
    UNKNOWN = None
    IPV4 = 4
    IPV6 = 6

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


class IP(LayerConfig):

    layer_type = LayerLevel.NETWORK
    layer_name = "IP"
    data: dict[str, Any]

    def __init__(
            self,
            version: IPVersion,
            src_addr: str,
            dst_addr: str,
            checksum_valid: bool | None) -> None:

        self.data = {
            "src_addr": src_addr,
            "dst_addr": dst_addr,
            "version": version,
            "checksum_valid": checksum_valid
        }
