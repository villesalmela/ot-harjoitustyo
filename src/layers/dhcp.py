from typing import Any
from layers.layer_config import LayerConfig
from layers.layer_level import LayerLevel
from components.enum_property import EnumProperty


class DHCPMessageType(EnumProperty):
    """Property of DHCP layer, holding Message Type.
    
    Will not raise ValueError if called with invalid value, returns None instead.
    Generated with ChatGPT."""
    DHCPDISCOVER = 1
    DHCPOFFER = 2
    DHCPREQUEST = 3
    DHCPDECLINE = 4
    DHCPACK = 5
    DHCPNAK = 6
    DHCPRELEASE = 7
    DHCPINFORM = 8

class BOOTPOpCode(EnumProperty):
    """Property of BOOTP layer, holding BOOTP Operation Code.
    
    Will not raise ValueError if called with invalid value, returns None instead.
    Generated with ChatGPT."""
    BOOTREQUEST = 1  # Used by a client to request configuration from servers
    BOOTREPLY = 2    # Used by a server to reply to a client's request

class DHCP(LayerConfig):
    """Configuration for DHCP layer."""

    layer_type = LayerLevel.APPLICATION
    layer_name = "DHCP"
    data: dict[str, Any]

    def __init__(self, protocol_data: dict[str, Any],
                 client_data: dict[str, Any],
                 server_data: dict[str, Any],
                 network_data: dict[str, Any]) -> None:
        """Initializes DHCP configuration object with provided details.

        Args:
            protocol_data (dict[str, Any]): operation, message_type, transaction_id
            client_data (dict[str, Any]): client_ip_current, client_ip_assigned, client_mac, client_hostname
            server_data (dict[str, Any]): server_ip, server_hostname
            network_data (dict[str, Any]): domain, name_server, router
        """

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
            "router": network_data["router"]
        }

    @classmethod
    def get_db_types(cls) -> dict[str, str]:
        """Get the location and type of custom objects, that need to be adapted for database
        operations.

        Returns:
            dict[str, str]: column_name, class_name
        """
        out = {
            f"{cls.layer_type}.{cls.layer_name}.data.operation": BOOTPOpCode.__name__,
            f"{cls.layer_type}.{cls.layer_name}.data.message_type": DHCPMessageType.__name__
        }
        return out
