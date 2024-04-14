import unittest

from parser.pcap_parser import PcapParser
from properties.layer_type import LayerType
from properties.dhcp_message_type import DHCPMessageType
from properties.bootp_opcode import BOOTPOpCode


class TestDHCP(unittest.TestCase):

    def setUp(self) -> None:
        parser = PcapParser()
        self.parsed_packets = parser.parse_pcap("assets/dhcp.pcap")

    def test_dhcp_discover(self) -> None:
        dhcp_layer = self.parsed_packets[0].layers[LayerType.APPLICATION]
        self.assertEqual(dhcp_layer.data, {
            "operation": BOOTPOpCode.BOOTREQUEST,
            "message_type": DHCPMessageType.DHCPDISCOVER,
            "transaction_id": 5468,
            "client_ip_current": "0.0.0.0",
            "client_ip_assigned": "0.0.0.0",
            "client_mac": "cc:00:0a:c4",
            "client_hostname": "R0",
            "server_ip": "0.0.0.0",
            "server_hostname": "",
            "domain": "",
            "name_server": "",
            "router": ""
        })

    def test_dhcp_offer(self) -> None:
        dhcp_layer = self.parsed_packets[1].layers[LayerType.APPLICATION]
        self.assertEqual(dhcp_layer.data, {
            "operation": BOOTPOpCode.BOOTREPLY,
            "message_type": DHCPMessageType.DHCPOFFER,
            "transaction_id": 5468,
            "client_ip_current": "0.0.0.0",
            "client_ip_assigned": "192.168.0.3",
            "client_mac": "cc:00:0a:c4",
            "client_hostname": "",
            "server_ip": "0.0.0.0",
            "server_hostname": "",
            "domain": "",
            "name_server": "192.168.0.1",
            "router": "192.168.0.1"
        })

    def test_dhcp_request(self) -> None:
        dhcp_layer = self.parsed_packets[2].layers[LayerType.APPLICATION]
        self.assertEqual(dhcp_layer.data, {
            "operation": BOOTPOpCode.BOOTREQUEST,
            "message_type": DHCPMessageType.DHCPREQUEST,
            "transaction_id": 5468,
            "client_ip_current": "0.0.0.0",
            "client_ip_assigned": "0.0.0.0",
            "client_mac": "cc:00:0a:c4",
            "client_hostname": "R0",
            "server_ip": "0.0.0.0",
            "server_hostname": "",
            "domain": "",
            "name_server": "",
            "router": ""
        })

    def test_dhcp_ack(self) -> None:
        dhcp_layer = self.parsed_packets[3].layers[LayerType.APPLICATION]
        self.assertEqual(dhcp_layer.data, {
            "operation": BOOTPOpCode.BOOTREPLY,
            "message_type": DHCPMessageType.DHCPACK,
            "transaction_id": 5468,
            "client_ip_current": "0.0.0.0",
            "client_ip_assigned": "192.168.0.3",
            "client_mac": "cc:00:0a:c4",
            "client_hostname": "R0",
            "server_ip": "0.0.0.0",
            "server_hostname": "",
            "domain": "",
            "name_server": "192.168.0.1",
            "router": "192.168.0.1"
        })
