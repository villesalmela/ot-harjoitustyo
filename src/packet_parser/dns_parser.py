from scapy.layers.dns import DNS
from layers.dns import DNS as myDNS, DNSDir, DNSOpCode, DNSQType, DNSRCode


class DNSParser:
    """Parser for DNS packets."""

    @classmethod
    def parse_dns(cls, dns_layer: DNS) -> tuple[myDNS, int, int]:
        if dns_layer.qd:
            qtype = DNSQType(dns_layer.qd.qtype)
            qname = dns_layer.qd.qname
        else:
            qtype = None
            qname = None
        if DNSDir(dns_layer.qr) == DNSDir.RESPONSE:
            answers = cls.parse_dns_answers(dns_layer)
            rcode = DNSRCode(dns_layer.rcode)
            if not answers:
                answers = None
        else:
            answers = None
            rcode = None
        return myDNS(
            dns_layer.id,
            DNSDir(dns_layer.qr), DNSOpCode(dns_layer.opcode),
            qtype,
            rcode,
            qname,
            answers
        ), len(dns_layer), len(dns_layer.payload)

    @staticmethod
    def parse_dns_answers(dns_layer) -> list[dict[str, str | int]]:
        """Parse DNS answers from the DNS layer.

        Args:
            dns_layer (_type_): The DNS layer

        Returns:
            list[dict[str, str | int]]: List of dictionaries with answer details
        """
        answers = []
        answer_rr = dns_layer.an  # Start with the first answer in the response
        while answer_rr:
            answers.append(answer_rr.fields.copy())
            answer_rr = answer_rr.payload  # Move to the next answer, if any
            if not answer_rr:  # Stop if no more answers
                break
        return answers
