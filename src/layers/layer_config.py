from abc import ABC, abstractmethod

from layers.layer_level import LayerLevel


class LayerConfig(ABC):
    """Base class for layer configuration objects."""

    layer_type: LayerLevel
    layer_name: str
    data: str
    dtypes: dict[str, type]

    @abstractmethod
    def __init__(self) -> None:
        pass
