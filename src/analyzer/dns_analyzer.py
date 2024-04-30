import pandas as pd

from layers.dns import DNSDir
from layers.layer_level import LayerLevel
from utils.utils import extract_2ld


class DNSAnalyzer:
    """Analyzer for producing statistics about DHCP packets."""

    def __init__(self, packets: pd.DataFrame) -> None:
        """Initializes the analyzer with provided packets and filters out all but selected DNS
        packets.

        Args:     packets (pd.DataFrame): one packet per row
        """
        selector = packets[f"{LayerLevel.APPLICATION}.layer_name"] == "DNS"
        self.packets = packets[selector]

        if self.packets.empty:
            return

        self.enrich()

    def enrich(self) -> None:
        """Enrich the packet data with new calculated fields.

        Parses Second Level Domain from the queried name and saves it in "2LD" column.
        """
        qname_series = self.packets.loc[:, f"{LayerLevel.APPLICATION}.DNS.data.qname"]
        sld_series = qname_series.apply(extract_2ld)
        self.packets.loc[:, f"{LayerLevel.APPLICATION}.DNS.data.2LD"] = sld_series

    def most_queried_domains(self, n=10) -> dict[str, int]:
        """Get the most commonly queried domains, grouped by second level domain.

        Args:     n (int, optional): How many domains to return. Defaults to 10.

        Returns:     dict[str, int]: domain, count
        """
        if self.packets.empty:
            return {}
        selector = f"{LayerLevel.APPLICATION}.DNS.data.2LD"
        return self.packets[selector].value_counts().head(n).to_dict()

    def most_common_servers(self, n=10) -> dict[str, int]:
        """Get the most commonly used DNS servers.

        Args:     n (int, optional): How many servers to return. Defaults to 10.

        Returns:     dict[str, int]: IP, count
        """
        if self.packets.empty:
            return {}

        selector = self.packets[f"{LayerLevel.APPLICATION}.DNS.data.direction"] == DNSDir.QUERY
        df = self.packets[selector]
        selector = f"{LayerLevel.NETWORK}.IP.data.dst_addr"
        return df[selector].value_counts().head(n).to_dict()
