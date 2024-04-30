from typing import Any

from layers.layer_config import LayerConfig
from layers.layer_level import LayerLevel
from components.enum_property import EnumProperty


class IPVersion(EnumProperty):
    """Property of IP layer, holding the version number.
    
    Will not raise ValueError if called with invalid value, returns None instead."""
    IPV4 = 4
    IPV6 = 6

class IP(LayerConfig):
    """Configuration for IP layer."""

    layer_type = LayerLevel.NETWORK
    layer_name = "IP"
    data: dict[str, Any]

    def __init__(
            self,
            version: IPVersion,
            src_addr: str,
            dst_addr: str,
            checksum_valid: bool | None) -> None:
        """Initializes IP configuration object with provided details.

        Args:
            version (IPVersion): either v4 or v6
            src_addr (str): source address
            dst_addr (str): destination address
            checksum_valid (bool | None): True if checksum is valid, False otherwise (only for v4).
        """

        self.data = {
            "src_addr": src_addr,
            "dst_addr": dst_addr,
            "version": version,
            "checksum_valid": checksum_valid
        }
