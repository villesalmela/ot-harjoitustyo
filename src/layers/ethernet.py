from layers.layer_config import LayerConfig
from properties.layer_level import LayerLevel


class Ethernet(LayerConfig):
    def __init__(self, src_addr: str, dst_addr: str) -> None:

        super().__init__(LayerLevel.LINK, "Ethernet", {
            "src_addr": src_addr,
            "dst_addr": dst_addr
        })
