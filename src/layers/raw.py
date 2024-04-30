from layers.layer_config import LayerConfig
from layers.layer_level import LayerLevel


class RAW(LayerConfig):
    """Configuration for RAW layer.
    
    This layer is used when no other layer is applicable."""

    layer_name = "RAW"
    layer_type: LayerLevel
    data: dict

    def __init__(self, layer_type: LayerLevel) -> None:
        """Initializes RAW configuration object with the provided layer level.

        Args:
            layer_type (LayerLevel): The position of this layer in the network stack
        """

        self.layer_type = layer_type
        self.data = {}
