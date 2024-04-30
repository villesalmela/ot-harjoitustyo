from typing import Self
import json

from layers.layer_config import LayerConfig
from utils.utils import preprocess_data, JSONEncoder


class Layer:
    """Stores a single network layer of a packet.
    """

    def __init__(self, config: LayerConfig, size_total: int, size_payload: int) -> None:
        """Initializes the layer with provided configuration and size information.

        Args:
            config (LayerConfig): a configuration object
            size_total (int): total size of the layer in bytes
            size_payload (int): size of the layer's payload in bytes
        """
        self.size_total = size_total
        self.size_payload = size_payload
        self.layer_name = config.layer_name
        self.data = preprocess_data(config.data)

    def __str__(self) -> str:
        """Get the string representation of this layer.

        Returns:
            str: name, size and other details
        """
        data = json.dumps(self.data, cls=JSONEncoder, indent=4)
        return f"name = {self.layer_name}\n" + f"size_total = {self.size_total}\n" + \
            f"size_payload = {self.size_payload}\n" + f"data = {data}\n"

    def __eq__(self, value: Self) -> bool:
        """Check if this layer equals another layer.

        Args:
            value (Self): The other layer

        Returns:
            bool: True if layers are equal, False otherwise
        """
        if not isinstance(value, Layer):
            return False
        return self.layer_name == value.layer_name and \
            self.data == value.data and \
            self.size_total == value.size_total and \
            self.size_payload == value.size_payload
