from layer_config import LayerConfig
from layer_type import LayerType


class DNS(LayerConfig):
    def __init__(self, direction: int, opcode: int, qtype: int, name: str,
                 answer: list[dict[str, str | int]] | None = None) -> None:

        super().__init__(LayerType.APPLICATION, "DNS", {
            "direction": direction,
            "opcode": opcode,
            "qtype": qtype,
            "name": name,
            "answer": answer
        })
