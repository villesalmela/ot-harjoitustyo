import unittest
from datetime import datetime

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

    def test_dns_layer_query_data(self) -> None:
        dns_layer = self.parsed_packets[0].layers[LayerType.APPLICATION]
        self.assertEqual(dns_layer.data["direction"], DNSDir.QUERY)
        self.assertEqual(dns_layer.data["opcode"], DNSOpCode.QUERY)
        self.assertEqual(dns_layer.data["qtype"], DNSQType.TXT)
        self.assertEqual(dns_layer.data["name"], "google.com.")
        self.assertIsNone(dns_layer.data["answer"])

    def test_dns_layer_response_data(self) -> None:
        dns_layer = self.parsed_packets[1].layers[LayerType.APPLICATION]
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

    def test_packet_str(self) -> None:
        self.maxDiff = None
        packet_str = str(self.parsed_packets[0])
        expected = """### PACKET START ###
time = 2005-03-30 11:47:46.496046
size = 70

LINK
name = Ethernet
size_total = 70
size_payload = 56
data = {'src_addr': '00:e0:18:b1:0c:ad', 'dst_addr': '00:c0:9f:32:41:8c'}

NETWORK
name = IP
size_total = 56
size_payload = 36
data = {'src_addr': '192.168.170.8', 'dst_addr': '192.168.170.20'}

TRANSPORT
name = UDP
size_total = 36
size_payload = 28
data = {'src_port': 32795, 'dst_port': 53}

APPLICATION
name = DNS
size_total = 28
size_payload = 0
data = {'direction': <DNSDir.QUERY: 0>, 'opcode': <DNSOpCode.QUERY: 0>, 'qtype': <DNSQType.TXT: 16>, 'name': 'google.com.', 'answer': None}
### PACKET END ###\n"""
        self.assertEqual(packet_str, expected)

    def test_packet(self) -> None:
        packet = self.parsed_packets[0]
        self.assertEqual(packet.size, 70)
        self.assertEqual(packet.time, datetime(2005, 3, 30, 11, 47, 46, 496046))
        self.assertTrue(packet == packet)
        self.assertFalse(packet == 1)

    def test_layer(self) -> None:
        layer = self.parsed_packets[0].layers[LayerType.APPLICATION]
        self.assertEqual(layer.size_total, 28)
        self.assertEqual(layer.size_payload, 0)
        self.assertEqual(layer.layer_type, LayerType.APPLICATION)
        self.assertEqual(layer.name, "DNS")
        self.assertTrue(layer == layer)
        self.assertFalse(layer == 1)

