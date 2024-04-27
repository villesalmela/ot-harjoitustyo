from typing import Any

from layers.layer_config import LayerConfig
from layers.layer_level import LayerLevel


class TCP(LayerConfig):

    layer_type = LayerLevel.TRANSPORT
    layer_name = "TCP"
    data: dict[str, Any]

    def __init__(self, src_port: int, dst_port: int, checksum_valid: bool) -> None:
        self.data = {"src_port": src_port, "dst_port": dst_port, "checksum_valid": checksum_valid}
