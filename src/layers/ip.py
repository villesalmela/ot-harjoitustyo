from layers.layer_config import LayerConfig
from layers.layer_level import LayerLevel


class IP(LayerConfig):
    def __init__(self, src_addr: str, dst_addr: str) -> None:

        super().__init__(LayerLevel.NETWORK, "IP", {
            "src_addr": src_addr,
            "dst_addr": dst_addr
        })
