from layer_type import LayerType
from typing import Any

class LayerConfig:
    def __init__(self, layer_type: LayerType, name: str, data: dict[str, Any]) -> None:
        self.layer_type = layer_type
        self.name = name
        self.data = data