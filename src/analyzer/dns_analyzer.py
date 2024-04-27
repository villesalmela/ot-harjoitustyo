import pandas as pd

from layers.dns import DNSDir
from layers.layer_level import LayerLevel
from utils.utils import extract_2ld


class DNSAnalyzer:

    def __init__(self, packets: pd.DataFrame) -> None:

        # filter packets with DNS layer
        selector = packets[f"{LayerLevel.APPLICATION}.layer_name"] == "DNS"
        self.packets = packets[selector]

        if self.packets.empty:
            return

        self.enrich()

    def enrich(self) -> None:
        # parse 2LD from qname
        qname_series = self.packets.loc[:, f"{LayerLevel.APPLICATION}.DNS.data.qname"]
        sld_series = qname_series.apply(extract_2ld)
        self.packets.loc[:, f"{LayerLevel.APPLICATION}.DNS.data.2LD"] = sld_series

    def most_queried_domains(self, n=10) -> dict[str, int]:
        if self.packets.empty:
            return {}
        selector = f"{LayerLevel.APPLICATION}.DNS.data.2LD"
        return self.packets[selector].value_counts().head(n).to_dict()

    def most_common_servers(self, n=10) -> dict[str, int]:
        if self.packets.empty:
            return {}
        # consider only data.direction = DNSDir.QUERY
        selector = self.packets[f"{LayerLevel.APPLICATION}.DNS.data.direction"] == DNSDir.QUERY
        df = self.packets[selector]
        selector = f"{LayerLevel.NETWORK}.IP.data.dst_addr"
        return df[selector].value_counts().head(n).to_dict()
