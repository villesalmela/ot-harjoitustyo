import pandas as pd

from components.packet import Packet as myPacket
from layers.layer_level import LayerLevel
from utils.utils import flatten_dict


class DHCPAnalyzer:

    def __init__(self, packets: list[myPacket]) -> None:

        # filter packets with DHCP layer
        self.packets = [packet for packet in packets if LayerLevel.APPLICATION in packet.layers and
                        packet.layers[LayerLevel.APPLICATION].layer_name == "DHCP"]
        if not self.packets:
            return

        # create dataframes
        self.dhcp_df = pd.DataFrame([flatten_dict(packet.layers[LayerLevel.APPLICATION].__dict__)
                                    for packet in self.packets])

        self.ip_df = pd.DataFrame([flatten_dict(packet.layers[LayerLevel.NETWORK].__dict__)
                                   for packet in self.packets])

        # configure dataframes
        self.dhcp_df.set_index("packet_uid", inplace=True)
        self.ip_df.set_index("packet_uid", inplace=True)

        # join addr columns from ip_df to dns_df
        self.dhcp_df = self.dhcp_df.join(
            self.ip_df[["data.src_addr", "data.dst_addr"]], how="inner")

        self.enrich()

        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 300)

    def enrich(self) -> None:
        pass

    def most_common_clients(self, n=10) -> dict[tuple[str, str], int]:
        if not self.packets:
            return {}
        clients_df = self.dhcp_df[(self.dhcp_df["data.client_hostname"] != "")]
        return clients_df.groupby(["data.client_hostname", "data.client_mac"]).size().head(n).to_dict()
