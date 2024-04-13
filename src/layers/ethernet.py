from layer_config import LayerConfig
from layer_type import LayerType


class Ethernet(LayerConfig):
    def __init__(self, src_addr: str, dst_addr: str) -> None:

        super().__init__(LayerType.LINK, "Ethernet", {
            "src_addr": src_addr,
            "dst_addr": dst_addr
        })
