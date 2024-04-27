import pandas as pd

from layers.layer_level import LayerLevel
from layers.dhcp import DHCPMessageType


class DHCPAnalyzer:

    def __init__(self, packets: pd.DataFrame) -> None:

        # filter packets with DHCP layer
        self.packets = packets[packets[f"{LayerLevel.APPLICATION}.layer_name"] == "DHCP"]
        if self.packets.empty:
            return

        self.acks = self.packets[(
            self.packets[f"{LayerLevel.APPLICATION}.DHCP.data.message_type"]
            == DHCPMessageType.DHCPACK)]

        self.enrich()

    def enrich(self) -> None:
        pass

    def most_common_clients(self, n=10) -> dict[tuple[str, str], int]:
        if self.packets.empty:
            return {}
        return self.acks.groupby(
            [
                f"{LayerLevel.APPLICATION}.DHCP.data.client_hostname",
                f"{LayerLevel.APPLICATION}.DHCP.data.client_mac"
            ]).size().head(n).to_dict()

    def most_common_servers(self, n=10) -> dict[str, int]:
        if self.packets.empty:
            return {}
        return self.acks.groupby(
            [
                f"{LayerLevel.NETWORK}.IP.data.src_addr",
                f"{LayerLevel.LINK}.Ethernet.data.src_addr"
            ]).size().head(n).to_dict()

    def most_common_domains(self, n=10) -> dict[str, int]:
        if self.packets.empty:
            return {}
        return self.acks.groupby(
            f"{LayerLevel.APPLICATION}.DHCP.data.domain").size().head(n).to_dict()
