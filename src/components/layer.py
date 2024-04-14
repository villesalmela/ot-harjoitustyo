from typing import Self
import json

from layers.layer_config import LayerConfig
from utils.utils import preprocess_data, JSONEncoder


class Layer:
    def __init__(self, config: LayerConfig, size_total: int, size_payload: int) -> None:
        self.size_total = size_total
        self.size_payload = size_payload
        self.layer_type = config.layer_type
        self.name = config.name
        self.data = preprocess_data(config.data)

    def __str__(self) -> str:
        data = json.dumps(self.data, cls=JSONEncoder, indent=4)
        return f"name = {self.name}\n" + f"size_total = {self.size_total}\n" + \
            f"size_payload = {self.size_payload}\n" + f"data = {data}\n"

    def __eq__(self, value: Self) -> bool:
        if not isinstance(value, Layer):
            return False
        return self.layer_type == value.layer_type and \
            self.name == value.name and \
            self.data == value.data and \
            self.size_total == value.size_total and \
            self.size_payload == value.size_payload
