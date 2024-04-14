from layer_config import LayerConfig
from layer_type import LayerType
from dns_dir import DNSDir
from dns_opcode import DNSOpCode
from dns_qtype import DNSQType


class DNS(LayerConfig):
    def __init__(self,
                 transaction_id: int,
                 direction: DNSDir,
                 opcode: DNSOpCode,
                 qtype: DNSQType,
                 name: str,
                 answers: list[dict[str, str | int]] | None = None
                 ) -> None:

        super().__init__(LayerType.APPLICATION, "DNS", {
            "transaction_id": transaction_id,
            "direction": direction,
            "opcode": opcode,
            "qtype": qtype,
            "name": name,
            "answers": answers
        })
