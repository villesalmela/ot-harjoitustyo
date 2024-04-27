from enum import Enum
from inspect import isclass
from abc import ABC, abstractmethod
from typing import get_type_hints

from layers.layer_level import LayerLevel


class LayerConfig(ABC):

    layer_type: LayerLevel
    layer_name: str
    data: str

    @abstractmethod
    def __init__(self) -> None:
        pass

    @classmethod
    def get_db_types(cls) -> dict[str, str]:
        out = {}
        hints = get_type_hints(cls.__init__)
        for name, hint_type in hints.items():
            if isclass(hint_type) and issubclass(hint_type, Enum):
                out[f"{cls.layer_type}.{cls.layer_name}.data.{name}"] = hint_type.__name__
        return out
