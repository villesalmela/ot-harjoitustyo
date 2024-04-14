from layers.layer_config import LayerConfig
from layers.layer_level import LayerLevel


class TCP(LayerConfig):
    def __init__(self, src_port: int, dst_port: int) -> None:

        super().__init__(LayerLevel.TRANSPORT, "TCP", {
            "src_port": src_port,
            "dst_port": dst_port
        })
