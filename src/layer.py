from typing import Self

from layer_config import LayerConfig


class Layer:
    def __init__(self, config: LayerConfig, size_total: int, size_payload: int) -> None:
        self.size_total = size_total
        self.size_payload = size_payload
        self.layer_type = config.layer_type
        self.name = config.name
        self.data = config.data

    def __str__(self) -> str:
        return f"name = {self.name}\n" + f"size_total = {self.size_total}\n" + \
            f"size_payload = {self.size_payload}\n" + f"data = {self.data}\n"
    
    def __eq__(self, value: Self) -> bool:
        if not isinstance(value, Layer):
            return False
        return self.layer_type == value.layer_type and \
            self.name == value.name and \
            self.data == value.data and \
            self.size_total == value.size_total and \
            self.size_payload == value.size_payload
        
    
