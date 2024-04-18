from collections import Counter

from components.packet import Packet as myPacket
from layers.layer_level import LayerLevel
from layers.properties.dns_dir import DNSDir
from utils.utils import extract_2ld, flatten_dict
import pandas as pd


class DNSAnalyzer:

    def __init__(self, packets: list[myPacket]) -> None:

        # filter packets with DNS layer
        self.packets = [packet for packet in packets if packet.layers[LayerLevel.APPLICATION] and
                        packet.layers[LayerLevel.APPLICATION].layer_name == "DNS"]

        # create dataframes
        self.dns_df = pd.DataFrame([flatten_dict(packet.layers[LayerLevel.APPLICATION].__dict__)
                                    for packet in self.packets])

        self.ip_df = pd.DataFrame([flatten_dict(packet.layers[LayerLevel.NETWORK].__dict__)
                                   for packet in self.packets])

        # configure dataframes
        self.dns_df.set_index("packet_uid", inplace=True)
        self.ip_df.set_index("packet_uid", inplace=True)

        # join addr columns from ip_df to dns_df
        self.dns_df = self.dns_df.join(self.ip_df[["data.src_addr", "data.dst_addr"]], how="inner")

        self.enrich()

        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 300)
        print(self.dns_df)

    def enrich(self) -> None:
        # parse 2LD from qname
        self.dns_df["data.2LD"] = self.dns_df["data.qname"].apply(extract_2ld)

    def most_queried_domains(self, n=10) -> dict[str, int]:
        return self.dns_df["data.2LD"].value_counts().head(n).to_dict()

    def most_common_servers(self, n=10) -> dict[str, int]:
        # consider only data.direction = DNSDir.QUERY
        return self.dns_df[self.dns_df["data.direction"] ==
                           DNSDir.QUERY]["data.dst_addr"].value_counts().head(n).to_dict()
