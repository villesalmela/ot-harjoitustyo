from typing import Any

from layers.layer_config import LayerConfig
from layers.layer_level import LayerLevel


class TCP(LayerConfig):
    """Configuration for TCP layer."""

    layer_type = LayerLevel.TRANSPORT
    layer_name = "TCP"
    data: dict[str, Any]

    def __init__(self, src_port: int, dst_port: int, checksum_valid: bool) -> None:
        """Initializes TCP configuration object with provided details.

        Args:
            src_port (int): source port
            dst_port (int): destination port
            checksum_valid (bool): True if checksum is valid, False otherwise
        """
        self.data = {"src_port": src_port, "dst_port": dst_port, "checksum_valid": checksum_valid}
