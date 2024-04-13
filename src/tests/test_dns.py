import unittest

from layers.dns import DNS
from main import parse_pcap, count_dns_domains, extract_2ld
from layer_type import LayerType
from dns_dir import DNSDir
from dns_opcode import DNSOpCode
from dns_qtype import DNSQType


class TestDNS(unittest.TestCase):
    def setUp(self) -> None:
        self.parsed_packets = parse_pcap("assets/dns.pcap")

    def test_count_dns_domains(self) -> None:
        domain_counts = count_dns_domains(self.parsed_packets)
        self.assertEqual(domain_counts["google.com"], 5)
        self.assertEqual(domain_counts["isc.org"], 2)

    def test_dns_layer_query(self) -> None:
        dns_layer = self.parsed_packets[0].layers[LayerType.APPLICATION]
        self.assertEqual(dns_layer.name, "DNS")
        self.assertEqual(dns_layer.data["direction"], DNSDir.QUERY)
        self.assertEqual(dns_layer.data["opcode"], DNSOpCode.QUERY)
        self.assertEqual(dns_layer.data["qtype"], DNSQType.TXT)
        self.assertEqual(dns_layer.data["name"], "google.com.")
        self.assertIsNone(dns_layer.data["answer"])

    def test_dns_layer_response(self) -> None:
        dns_layer = self.parsed_packets[1].layers[LayerType.APPLICATION]
        self.assertEqual(dns_layer.name, "DNS")
        self.assertEqual(dns_layer.data["direction"], DNSDir.RESPONSE)
        self.assertEqual(dns_layer.data["opcode"], DNSOpCode.QUERY)
        self.assertEqual(dns_layer.data["qtype"], DNSQType.TXT)
        self.assertEqual(dns_layer.data["name"], "google.com.")
        self.assertEqual(dns_layer.data["answer"],
                         [{'rrname': 'google.com.',
                           'type': 16,
                           'rclass': 1,
                           'ttl': 270,
                           'rdlen': 16,
                           'rdata': [b'v=spf1 ptr ?all']}])
        
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

    
