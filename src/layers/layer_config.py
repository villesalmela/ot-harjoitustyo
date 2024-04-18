from typing import Any
from layers.layer_level import LayerLevel


class LayerConfig:
    def __init__(self, layer_type: LayerLevel, layer_name: str, data: dict[str, Any]) -> None:
        self.layer_type = layer_type
        self.layer_name = layer_name
        self.data = data
