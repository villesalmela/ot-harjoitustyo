from layers.layer_config import LayerConfig
from layers.layer_level import LayerLevel


class Ethernet(LayerConfig):
    """Configuration for Ethernet layer."""

    layer_type = LayerLevel.LINK
    layer_name = "Ethernet"
    data: dict[str, str]

    def __init__(self, src_addr: str, dst_addr: str) -> None:
        """Initializes Ethernet configuration object with provided details.

        Args:
            src_addr (str): source address
            dst_addr (str): destination address
        """

        self.data = {
            "src_addr": src_addr,
            "dst_addr": dst_addr
        }
