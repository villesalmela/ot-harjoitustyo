import unittest
from datetime import datetime


from packet_parser.pcap_parser import PcapParser
from layers.layer_level import LayerLevel


ASSET_PATH = "assets/dns.pcapng"


class TestPacket(unittest.TestCase):

    def setUp(self) -> None:
        parser = PcapParser()
        self.parsed_packets = parser.parse_pcap(ASSET_PATH)

    def test_packet(self) -> None:
        packet = self.parsed_packets[0]
        self.assertEqual(packet.size, 70)
        self.assertEqual(packet.time, datetime(2023, 2, 6, 20, 16, 7))
        self.assertTrue(packet == packet)
        self.assertFalse(packet == 1)

    def test_layer(self) -> None:
        layer = self.parsed_packets[0].layers[LayerLevel.APPLICATION]
        self.assertEqual(layer.size_total, 28)
        self.assertEqual(layer.size_payload, 0)
        self.assertEqual(layer.layer_name, "DNS")
        self.assertTrue(layer == layer)
        self.assertFalse(layer == 1)
