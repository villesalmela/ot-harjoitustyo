import unittest

from main import parse_pcap
from layer_type import LayerType
from dhcp_message_type import DHCPMessageType
from bootp_opcode import BOOTPOpCode


class TestDHCP(unittest.TestCase):

    def setUp(self) -> None:
        self.parsed_packets = parse_pcap("assets/dhcp.pcap")

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
