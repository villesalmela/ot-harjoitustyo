from typing import Any
from layers.layer_config import LayerConfig
from layers.layer_level import LayerLevel


class DHCP(LayerConfig):
    def __init__(self, protocol_data: dict[str, Any],
                 client_data: dict[str, Any],
                 server_data: dict[str, Any],
                 network_data: dict[str, Any]) -> None:

        super().__init__(LayerLevel.APPLICATION, "DHCP", {
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

        })
