import unittest
from layers.layer_level import LayerLevel

from main import Context
from analyzer.base_analyzer import BaseAnalyzer


class TestProtocols(unittest.TestCase):

    def setUp(self) -> None:
        self.context = Context(reset_db=True)
        self.context.append("assets/combo.pcapng")
        self.storage = self.context.storage
        self.df = self.context.get_df()
        self.base_analyzer = BaseAnalyzer(self.df)

    def tearDown(self) -> None:
        self.storage.conn.close()

    def test_distribution(self) -> None:
        expected_application = {'DHCP': 10, 'DNS': 32, 'RAW': 118}
        expected_transport = {'ICMP': 41, 'RAW': 64, 'UDP': 55}
        expected_network = {'ARP': 1, 'IP': 117, 'RAW': 42}
        expected_link = {'Ethernet': 146, 'RAW': 2, 'SLL': 12}

        application = self.base_analyzer.protocol_distribution()[LayerLevel.APPLICATION].to_dict()
        transport = self.base_analyzer.protocol_distribution()[LayerLevel.TRANSPORT].to_dict()
        network = self.base_analyzer.protocol_distribution()[LayerLevel.NETWORK].to_dict()
        link = self.base_analyzer.protocol_distribution()[LayerLevel.LINK].to_dict()

        self.assertEqual(application, expected_application)
        self.assertEqual(transport, expected_transport)
        self.assertEqual(network, expected_network)
        self.assertEqual(link, expected_link)
