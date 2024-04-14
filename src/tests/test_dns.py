import unittest

from parser.pcap_parser import PcapParser
from analyzer.dns_analyzer import DNSAnalyzer
from utils.utils import extract_2ld
from properties.layer_type import LayerType
from properties.dns_dir import DNSDir
from properties.dns_opcode import DNSOpCode
from properties.dns_qtype import DNSQType


class TestDNS(unittest.TestCase):
    def setUp(self) -> None:
        parser = PcapParser()
        self.parsed_packets = parser.parse_pcap("assets/dns.pcap")

    def test_count_dns_domains(self) -> None:
        domain_counts = DNSAnalyzer.count_dns_domains(self.parsed_packets)
        self.assertEqual(domain_counts["google.com"], 5)
        self.assertEqual(domain_counts["isc.org"], 2)

    def test_dns_layer_query_data(self) -> None:
        dns_layer = self.parsed_packets[0].layers[LayerType.APPLICATION]
        self.assertEqual(dns_layer.data, {
            "transaction_id": 4146,
            "direction": DNSDir.QUERY,
            "opcode": DNSOpCode.QUERY,
            "qtype": DNSQType.TXT,
            "name": "google.com.",
            "answers": None
        })

    def test_dns_layer_response_data(self) -> None:
        dns_layer = self.parsed_packets[1].layers[LayerType.APPLICATION]
        self.assertEqual(dns_layer.data, {
            "transaction_id": 4146,
            "direction": DNSDir.RESPONSE,
            "opcode": DNSOpCode.QUERY,
            "qtype": DNSQType.TXT,
            "name": "google.com.",
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
        with self.assertRaises(ValueError):
            extract_2ld("")

    def test_2ld_extraction_fallback_invalid_tld_normal(self) -> None:
        domain = extract_2ld("www.google.invalid")
        self.assertEqual(domain, "google.invalid")

    def test_2ld_extraction_fallback_invalid_tld_no_effect(self) -> None:
        domain = extract_2ld("google.invalid")
        self.assertEqual(domain, "google.invalid")
