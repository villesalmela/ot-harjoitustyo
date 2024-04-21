from layers.layer_config import LayerConfig
from layers.layer_level import LayerLevel
from layers.properties.icmp_code import ICMPCode, ICMPType
from layers.properties.icmpv6_code import ICMPv6Code, ICMPv6Type
from layers.properties.icmp_version import ICMPVersion


class ICMP(LayerConfig):
    def __init__(
            self,
            version: ICMPVersion,
            icmp_type: ICMPType | ICMPv6Type,
            icmp_code: ICMPCode | ICMPv6Code,
            seq: int | None,
            identifier: int | None,
            checksum_valid: bool) -> None:

        super().__init__(LayerLevel.TRANSPORT, version.name, {
            "icmp_type": icmp_type,
            "icmp_code": icmp_code,
            "seq": seq,
            "identifier": identifier,
            "checksum_valid": checksum_valid
        })
