import pandas as pd

from layers.layer_level import LayerLevel
from layers.dhcp import DHCPMessageType


class DHCPAnalyzer:
    """Analyzer for producing statistics about DHCP packets."""

    def __init__(self, packets: pd.DataFrame) -> None:
        """Initializes the analyzer with provided packets and filters out all but selected DHCP
        packets.

        Args:
            packets (pd.DataFrame): one packet per row
        """
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

    def most_common_clients(self, n=10) -> dict[tuple[str, str], int]:
        """From the clients that have done DHCP requests, return "n" most common ones.

        Args:
            n (int, optional): How many clients to return. Defaults to 10.

        Returns:
            dict[tuple[str, str], int]: (hostname, MAC), count
        """
        if self.packets.empty:
            return {}
        selector = [
            f"{LayerLevel.APPLICATION}.DHCP.data.client_hostname",
            f"{LayerLevel.APPLICATION}.DHCP.data.client_mac"
        ]
        return self.acks.groupby(selector).size().head(n).to_dict()

    def most_common_servers(self, n=10) -> dict[str, int]:
        """From the servers that have returned DHCPACKs, return the "n" most common ones.

        Args:
            n (int, optional): How manu servers to return. Defaults to 10.

        Returns:
            dict[str, int]: (IP, MAC), count
        """
        if self.packets.empty:
            return {}
        selector = [
            f"{LayerLevel.NETWORK}.IP.data.src_addr",
            f"{LayerLevel.LINK}.Ethernet.data.src_addr"
        ]
        return self.acks.groupby(selector).size().head(n).to_dict()

    def most_common_domains(self, n=10) -> dict[str, int]:
        """From the DHCPACK packets, return the "n" most common domains.

        Args:
            n (int, optional): How many domains to return. Defaults to 10.

        Returns:
            dict[str, int]: domain, count
        """
        if self.packets.empty:
            return {}
        selector = f"{LayerLevel.APPLICATION}.DHCP.data.domain"
        return self.acks.groupby(selector).size().head(n).to_dict()
