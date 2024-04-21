from layers.layer_config import LayerConfig
from layers.layer_level import LayerLevel
from layers.properties.ip_version import IPVersion


class IP(LayerConfig):
    def __init__(
            self,
            version: IPVersion,
            src_addr: str,
            dst_addr: str,
            checksum_valid: bool | None) -> None:

        if version == IPVersion.IPV4:
            super().__init__(LayerLevel.NETWORK, version.name, {
                "src_addr": src_addr,
                "dst_addr": dst_addr,
                "checksum_valid": checksum_valid
            })
        elif version == IPVersion.IPV6:
            super().__init__(LayerLevel.NETWORK, version.name, {
                "src_addr": src_addr,
                "dst_addr": dst_addr
            })
        else:
            raise ValueError(f"Unsupported IP version: {version}")
