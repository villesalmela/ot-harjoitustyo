import unittest
from datetime import datetime

from main import parse_pcap
from layer_type import LayerType


class TestPacket(unittest.TestCase):

    def setUp(self) -> None:
        self.parsed_packets = parse_pcap("assets/dns.pcap")

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
