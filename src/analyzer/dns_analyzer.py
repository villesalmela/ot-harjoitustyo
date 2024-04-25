import pandas as pd

from layers.properties.dns_dir import DNSDir
from layers.layer_level import LayerLevel
from utils.utils import extract_2ld


class DNSAnalyzer:

    def __init__(self, packets: pd.DataFrame) -> None:

        # filter packets with DNS layer
        self.packets = packets[packets[f"{LayerLevel.APPLICATION}.layer_name"] == "DNS"]

        if self.packets.empty:
            return

        self.enrich()

    def enrich(self) -> None:
        # parse 2LD from qname
        self.packets[f"{LayerLevel.APPLICATION}.data.2LD"] = self.packets[
            "APPLICATION.data.qname"].apply(extract_2ld)

    def most_queried_domains(self, n=10) -> dict[str, int]:
        if self.packets.empty:
            return {}
        return self.packets[f"{LayerLevel.APPLICATION}.data.2LD"].value_counts().head(n).to_dict()

    def most_common_servers(self, n=10) -> dict[str, int]:
        if self.packets.empty:
            return {}
        # consider only data.direction = DNSDir.QUERY
        df = self.packets[self.packets[f"{LayerLevel.APPLICATION}.data.direction"] == DNSDir.QUERY]
        return df[f"{LayerLevel.NETWORK}.data.dst_addr"].value_counts().head(n).to_dict()
