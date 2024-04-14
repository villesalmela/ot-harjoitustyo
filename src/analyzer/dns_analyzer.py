from collections import Counter

from components.packet import Packet as myPacket
from properties.layer_type import LayerType
from properties.dns_dir import DNSDir
from utils.utils import extract_2ld


class DNSAnalyzer:

    @staticmethod
    def count_dns_domains(packets: list[myPacket]) -> dict[str, int]:
        """Return a counter object containing number of queries per domain name."""
        counter = Counter()
        for packet in packets:
            dns_layer = packet.layers[LayerType.APPLICATION]
            if dns_layer and dns_layer.name == "DNS" and dns_layer.data["direction"] == DNSDir.QUERY:
                fqdn = dns_layer.data["name"].strip(".")
                domain = extract_2ld(fqdn)
                counter[domain] += 1
        return dict(counter)