from layer_config import LayerConfig
from layer_type import LayerType

class TCP(LayerConfig):
    def __init__(self, src_port: int, dst_port: int) -> None:
        
        super().__init__(LayerType.TRANSPORT, "TCP", {
            "src_port": src_port,
            "dst_port": dst_port
        })