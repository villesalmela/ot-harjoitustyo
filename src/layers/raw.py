from layers.layer_config import LayerConfig
from layers.layer_level import LayerLevel


class RAW(LayerConfig):
    def __init__(self, layer_level: LayerLevel) -> None:

        super().__init__(layer_level, "RAW", {})
