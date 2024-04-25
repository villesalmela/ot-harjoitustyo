import pandas as pd

from layers.layer_level import LayerLevel


class DHCPAnalyzer:

    def __init__(self, packets: pd.DataFrame) -> None:

        # filter packets with DHCP layer
        self.packets = packets[packets[f"{LayerLevel.APPLICATION}.layer_name"] == "DHCP"]
        if self.packets.empty:
            return

        self.enrich()

    def enrich(self) -> None:
        pass

    def most_common_clients(self, n=10) -> dict[tuple[str, str], int]:
        if self.packets.empty:
            return {}
        clients_df = self.packets[(
            self.packets[f"{LayerLevel.APPLICATION}.data.client_hostname"] != "")]
        return clients_df.groupby(
            [
                f"{LayerLevel.APPLICATION}.data.client_hostname",
                f"{LayerLevel.APPLICATION}.data.client_mac"
            ]).size().head(n).to_dict()
