import unittest

from packet_parser.pcap_parser import PcapParser
from analyzer.dns_analyzer import DNSAnalyzer
from utils.utils import extract_2ld
from layers.layer_level import LayerLevel
from layers.dns import DNSDir, DNSOpCode, DNSQType, DNSRCode
from main import Context


ASSET_PATH = "assets/dns.pcapng"


class TestDNS(unittest.TestCase):
    def setUp(self) -> None:
        parser = PcapParser()
        self.parsed_packets = parser.parse_pcap(ASSET_PATH)
        context = Context()
        context.append(ASSET_PATH)
        self.analyzer = DNSAnalyzer(context.get_df())

    def test_count_dns_domains(self) -> None:
        domain_counts = self.analyzer.most_queried_domains()
        self.assertEqual(domain_counts["google.com"], 10)
        self.assertEqual(domain_counts["isc.org"], 4)

    def test_count_dns_servers(self) -> None:
        server_counts = self.analyzer.most_common_servers()
        self.assertEqual(server_counts["217.13.4.24"], 5)
        self.assertEqual(server_counts["192.168.170.20"], 14)

    def test_dns_layer_query_data(self) -> None:
        dns_layer = self.parsed_packets[0].layers[LayerLevel.APPLICATION]
        self.assertEqual(dns_layer.data, {
            "transaction_id": 4146,
            "direction": DNSDir.QUERY,
            "opcode": DNSOpCode.QUERY,
            "qtype": DNSQType.TXT,
            "rcode": None,
            "qname": "google.com.",
            "answers": None
        })

    def test_dns_layer_response_data(self) -> None:
        dns_layer = self.parsed_packets[1].layers[LayerLevel.APPLICATION]
        self.assertEqual(dns_layer.data, {
            "transaction_id": 4146,
            "direction": DNSDir.RESPONSE,
            "opcode": DNSOpCode.QUERY,
            "qtype": DNSQType.TXT,
            "rcode": DNSRCode.NOERROR,
            "qname": "google.com.",
            "answers": [{'rrname': 'google.com.',
                         'type': 16,
                         'rclass': 1,
                         'ttl': 270,
                         'rdlen': 16,
                         'rdata': ['v=spf1 ptr ?all']}]
        })

    def test_2ld_extraction_normal(self) -> None:
        domain = extract_2ld("www.google.com")
        self.assertEqual(domain, "google.com")

    def test_2ld_extraction_no_effect(self) -> None:
        domain = extract_2ld("google.com")
        self.assertEqual(domain, "google.com")

    def test_2ld_extraction_fallback_single(self) -> None:
        domain = extract_2ld("localhost")
        self.assertEqual(domain, "localhost")

    def test_2ld_extraction_fallback_empty(self) -> None:
        self.assertEqual(extract_2ld(""), "")

    def test_2ld_extraction_fallback_invalid_tld_normal(self) -> None:
        domain = extract_2ld("www.google.invalid")
        self.assertEqual(domain, "google.invalid")

    def test_2ld_extraction_fallback_invalid_tld_no_effect(self) -> None:
        domain = extract_2ld("google.invalid")
        self.assertEqual(domain, "google.invalid")
