import pandas as pd

from layers.layer_level import LayerLevel
from layers.dhcp import DHCPMessageType


class DHCPAnalyzer:

    def __init__(self, packets: pd.DataFrame) -> None:

        # filter packets with DHCP layer
        selector = packets[f"{LayerLevel.APPLICATION}.layer_name"] == "DHCP"
        self.packets = packets[selector]
        if self.packets.empty:
            return

        selector = (
            self.packets[
                f"{LayerLevel.APPLICATION}.DHCP.data.message_type"
            ] == DHCPMessageType.DHCPACK
        )
        self.acks = self.packets[selector]

        self.enrich()

    def enrich(self) -> None:
        pass

    def most_common_clients(self, n=10) -> dict[tuple[str, str], int]:
        if self.packets.empty:
            return {}
        selector = [
            f"{LayerLevel.APPLICATION}.DHCP.data.client_hostname",
            f"{LayerLevel.APPLICATION}.DHCP.data.client_mac"
        ]
        return self.acks.groupby(selector).size().head(n).to_dict()

    def most_common_servers(self, n=10) -> dict[str, int]:
        if self.packets.empty:
            return {}
        selector = [
            f"{LayerLevel.NETWORK}.IP.data.src_addr",
            f"{LayerLevel.LINK}.Ethernet.data.src_addr"
        ]
        return self.acks.groupby(selector).size().head(n).to_dict()

    def most_common_domains(self, n=10) -> dict[str, int]:
        if self.packets.empty:
            return {}
        selector = f"{LayerLevel.APPLICATION}.DHCP.data.domain"
        return self.acks.groupby(selector).size().head(n).to_dict()
