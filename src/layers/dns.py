from layers.layer_config import LayerConfig
from layers.layer_level import LayerLevel
from layers.properties.dns_dir import DNSDir
from layers.properties.dns_opcode import DNSOpCode
from layers.properties.dns_qtype import DNSQType
from layers.properties.dns_rcode import DNSRCode


class DNS(LayerConfig):
    def __init__(self,
                 transaction_id: int,
                 direction: DNSDir,
                 opcode: DNSOpCode,
                 qtype: DNSQType | None,
                 rcode: DNSRCode,
                 qname: str | None,
                 answers: list[dict[str, str | int]] | None = None
                 ) -> None:

        super().__init__(LayerLevel.APPLICATION, "DNS", {
            "transaction_id": transaction_id,
            "direction": direction,
            "opcode": opcode,
            "qtype": qtype,
            "rcode": rcode,
            "qname": qname,
            "answers": answers
        })
