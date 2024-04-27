from typing import Any
from layers.layer_config import LayerConfig
from layers.layer_level import LayerLevel
from components.enum_property import EnumProperty


class DHCPMessageType(EnumProperty):
    "Generated with ChatGPT."
    UNKNOWN = None
    DHCPDISCOVER = 1
    DHCPOFFER = 2
    DHCPREQUEST = 3
    DHCPDECLINE = 4
    DHCPACK = 5
    DHCPNAK = 6
    DHCPRELEASE = 7
    DHCPINFORM = 8

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


class BOOTPOpCode(EnumProperty):
    "Generated with ChatGPT."
    UNKNOWN = None
    BOOTREQUEST = 1  # Used by a client to request configuration from servers
    BOOTREPLY = 2    # Used by a server to reply to a client's request

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


class DHCP(LayerConfig):

    layer_type = LayerLevel.APPLICATION
    layer_name = "DHCP"
    data: dict[str, Any]

    def __init__(self, protocol_data: dict[str, Any],
                 client_data: dict[str, Any],
                 server_data: dict[str, Any],
                 network_data: dict[str, Any]) -> None:

        self.data = {
            "operation": protocol_data["operation"],
            "message_type": protocol_data["message_type"],
            "transaction_id": protocol_data["transaction_id"],
            "client_ip_current": client_data["ip_current"],
            "client_ip_assigned": client_data["ip_assigned"],
            "client_mac": client_data["mac"],
            "client_hostname": client_data["hostname"],
            "server_ip": server_data["ip"],
            "server_hostname": server_data["hostname"],
            "domain": network_data["domain"],
            "name_server": network_data["name_server"],
            "router": network_data["router"],

        }

    @classmethod
    def get_db_types(cls) -> dict[str, str]:
        out = {
            f"{cls.layer_type}.{cls.layer_name}.data.operation": BOOTPOpCode.__name__,
            f"{cls.layer_type}.{cls.layer_name}.data.message_type": DHCPMessageType.__name__
        }

        return out
