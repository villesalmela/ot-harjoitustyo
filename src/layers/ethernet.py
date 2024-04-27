from layers.layer_config import LayerConfig
from layers.layer_level import LayerLevel


class Ethernet(LayerConfig):

    layer_type = LayerLevel.LINK
    layer_name = "Ethernet"
    data: dict[str, str]

    def __init__(self, src_addr: str, dst_addr: str) -> None:

        self.data = {
            "src_addr": src_addr,
            "dst_addr": dst_addr
        }
