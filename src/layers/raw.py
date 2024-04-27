from layers.layer_config import LayerConfig
from layers.layer_level import LayerLevel


class RAW(LayerConfig):

    layer_name = "RAW"
    layer_type: LayerLevel
    data: dict

    def __init__(self, layer_type: LayerLevel) -> None:

        self.layer_type = layer_type
        self.data = {}
