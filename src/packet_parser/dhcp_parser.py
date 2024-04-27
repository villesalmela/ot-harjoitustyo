from scapy.layers.dhcp import DHCP, BOOTP
from layers.dhcp import DHCP as myDHCP, DHCPMessageType, BOOTPOpCode
from utils.utils import convert_mac


class DHCPParser:

    @staticmethod
    def parse_dhcp(bootp_layer: BOOTP, dhcp_layer: DHCP) -> tuple[myDHCP, int, int]:
        def get_option(options, key):
            for option in options:
                if option[0] == key:
                    value = option[1]
                    if isinstance(value, bytes):
                        return value
                    return value
            return ""

        client_data = {
            "mac": convert_mac(bootp_layer.chaddr),
            "ip_current": bootp_layer.ciaddr,
            "ip_assigned": bootp_layer.yiaddr,
            "hostname": get_option(dhcp_layer.options, "hostname")
        }
        server_data = {
            "ip": bootp_layer.siaddr,
            "hostname": bootp_layer.sname
        }
        network_data = {
            "domain": get_option(dhcp_layer.options, "domain"),
            "name_server": get_option(dhcp_layer.options, "name_server"),
            "router": get_option(dhcp_layer.options, "router")
        }
        protocol_data = {
            "operation": BOOTPOpCode(bootp_layer.op),
            "message_type": DHCPMessageType(get_option(dhcp_layer.options, "message-type")),
            "transaction_id": bootp_layer.xid
        }
        return myDHCP(protocol_data, client_data, server_data, network_data), len(
            bootp_layer), len(dhcp_layer.payload)
