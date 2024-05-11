import unittest

from packet_parser.pcap_parser import PcapParser
from analyzer.dhcp_analyzer import DHCPAnalyzer
from layers.layer_level import LayerLevel
from layers.dhcp import DHCPMessageType, BOOTPOpCode
from main import Context


class TestDHCP(unittest.TestCase):

    def setUp(self) -> None:
        parser = PcapParser()
        self.parsed_packets = parser.parse_pcap("assets/dhcp.pcap")
        context = Context()
        context.append("assets/dhcp.pcap")
        self.analyzer = DHCPAnalyzer(context.get_df())

    def test_dhcp_client_count(self) -> None:
        client_counts = self.analyzer.most_common_clients()
        self.assertEqual(client_counts[("Microknoppix", "21:6a:2d:3b:8e")], 2)
        self.assertEqual(client_counts[("pi01-test1", "b8:27:eb:c9:16:37")], 4)

    def test_dhcp_server_count(self) -> None:
        server_counts = self.analyzer.most_common_servers()
        self.assertEqual(server_counts[("192.168.42.4", "00:15:62:6a:fe:f1")], 2)
        self.assertEqual(server_counts[("192.168.2.1", "d4:21:22:76:5b:78")], 1)

    def test_dhcp_domain_count(self) -> None:
        domain_counts = self.analyzer.most_common_domains()
        self.assertEqual(domain_counts["webernetz.net"], 1)
        self.assertEqual(domain_counts["weberlab.de"], 2)


    def test_dhcp_discover(self) -> None:
        dhcp_layer = self.parsed_packets[0].layers[LayerLevel.APPLICATION]
        self.assertEqual(dhcp_layer.data, {
            "operation": BOOTPOpCode.BOOTREQUEST,
            "message_type": DHCPMessageType.DHCPDISCOVER,
            "transaction_id": 3973631524,
            "client_ip_current": "0.0.0.0",
            "client_ip_assigned": "0.0.0.0",
            "client_mac": "21:6a:2d:3b:8e",
            "client_hostname": "Microknoppix",
            "server_ip": "0.0.0.0",
            "server_hostname": "",
            "domain": "",
            "name_server": "",
            "router": ""
        })

    def test_dhcp_offer(self) -> None:
        dhcp_layer = self.parsed_packets[1].layers[LayerLevel.APPLICATION]
        self.assertEqual(dhcp_layer.data, {
            "operation": BOOTPOpCode.BOOTREPLY,
            "message_type": DHCPMessageType.DHCPOFFER,
            "transaction_id": 3973631524,
            "client_ip_current": "0.0.0.0",
            "client_ip_assigned": "192.168.2.102",
            "client_mac": "21:6a:2d:3b:8e",
            "client_hostname": "",
            "server_ip": "0.0.0.0",
            "server_hostname": "",
            "domain": "Speedport_W_724V_09011603_00_009",
            "name_server": "192.168.2.1",
            "router": "192.168.2.1"
        })

    def test_dhcp_request(self) -> None:
        dhcp_layer = self.parsed_packets[2].layers[LayerLevel.APPLICATION]
        self.assertEqual(dhcp_layer.data, {
            "operation": BOOTPOpCode.BOOTREQUEST,
            "message_type": DHCPMessageType.DHCPREQUEST,
            "transaction_id": 3973631524,
            "client_ip_current": "0.0.0.0",
            "client_ip_assigned": "0.0.0.0",
            "client_mac": "21:6a:2d:3b:8e",
            "client_hostname": "Microknoppix",
            "server_ip": "0.0.0.0",
            "server_hostname": "",
            "domain": "",
            "name_server": "",
            "router": ""
        })

    def test_dhcp_ack(self) -> None:
        dhcp_layer = self.parsed_packets[3].layers[LayerLevel.APPLICATION]
        self.assertEqual(dhcp_layer.data, {
            "operation": BOOTPOpCode.BOOTREPLY,
            "message_type": DHCPMessageType.DHCPACK,
            "transaction_id": 3973631524,
            "client_ip_current": "0.0.0.0",
            "client_ip_assigned": "192.168.2.102",
            "client_mac": "21:6a:2d:3b:8e",
            "client_hostname": "",
            "server_ip": "0.0.0.0",
            "server_hostname": "",
            "domain": "Speedport_W_724V_09011603_00_009",
            "name_server": "192.168.2.1",
            "router": "192.168.2.1"
        })
