from typing import Any
from layers.layer_level import LayerLevel


class LayerConfig:
    def __init__(self, layer_type: LayerLevel, name: str, data: dict[str, Any]) -> None:
        self.layer_type = layer_type
        self.name = name
        self.data = data
