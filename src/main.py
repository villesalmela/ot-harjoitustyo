import pandas as pd

import config
from packet_parser.pcap_parser import PcapParser
from analyzer.dns_analyzer import DNSAnalyzer
from analyzer.dhcp_analyzer import DHCPAnalyzer
from analyzer.base_analyzer import BaseAnalyzer
from ui import ui
from ui.figure_config import FigureConfig
from utils.utils import scale_bits, convert_to_bits
from storage.database import DBStorage
from layers.layer_level import LayerLevel


pd.set_option('future.no_silent_downcasting', True)

# for debugging
# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
# pd.set_option('display.width', 300)


class Context:
    def __init__(self, reset_db=False) -> None:
        self.df = pd.DataFrame()
        self.storage = DBStorage(config.DB_PATH, reset=reset_db)

    def __len__(self):
        return len(self.df)

    def get_df(self):
        return self.df.copy()

    def reset(self):
        self.df = pd.DataFrame()

    def save(self, name: str):
        self.storage.save(self.df, name)

    def load(self, name: str):
        self.df = self.storage.load(name)

    def list_slots(self):
        return self.storage.list_slots()

    def del_slot(self, name: str):
        self.storage.del_slot(name)

    def append(self, filename: str):
        parsed_packets = PcapParser().parse_pcap(filename)

        flat_packets = []
        for packet in parsed_packets:
            flat_packet = packet.flatten()
            flat_packet.update({"packet.str": str(packet)})
            flat_packets.append(flat_packet)
        df = pd.DataFrame(flat_packets).set_index("packet.uid")
        self.df = pd.concat([self.df, df])
        self.df = DBStorage.adjust_dtypes(self.df)


def configure_speed_graph(base_analyzer: BaseAnalyzer) -> FigureConfig:
    # Get the time series data
    bytes_per_second, max_bytes_per_second = base_analyzer.time_series_speed(100)

    # Convert bytes to bits
    bits_per_second = convert_to_bits(bytes_per_second)
    max_bits_per_second = convert_to_bits(max_bytes_per_second)

    # Adjust the speed unit
    scaled_speed_max, unit_max = scale_bits(max_bits_per_second)
    scaled_speed, unit = scale_bits(bits_per_second)

    # Prepare figure configurations
    speed_config = FigureConfig(
        "Traffic speed",
        scaled_speed,
        "Time",
        f"Average Speed ({unit} per second)",
        "tab:blue",
        scaled_speed_max,
        f"Max Speed ({unit_max} per second)",
        "tab:red")

    return speed_config


def configure_dns_most_queried_domains(dns_analyzer: DNSAnalyzer) -> FigureConfig:
    dns_most_queried_domains = dns_analyzer.most_queried_domains()
    dns1_config = FigureConfig(
        "Most Queried Domains",
        dns_most_queried_domains,
        "Domain",
        "Count",
        "tab:blue")
    return dns1_config


def configure_dns_most_common_servers(dns_analyzer: DNSAnalyzer) -> FigureConfig:
    dns_most_common_servers = dns_analyzer.most_common_servers()
    dns2_config = FigureConfig(
        "Most Common Servers",
        dns_most_common_servers,
        "Server",
        "Count",
        "tab:red")
    return dns2_config


def configure_dhcp_most_common_clients(dhcp_analyzer: DHCPAnalyzer) -> FigureConfig:
    dhcp_most_common_clients = dhcp_analyzer.most_common_clients()
    dhcp_config = FigureConfig(
        "Most Common Clients",
        dhcp_most_common_clients,
        "Client",
        "Count",
        "tab:green")
    return dhcp_config


def configure_dhcp_most_common_servers(dhcp_analyzer: DHCPAnalyzer) -> FigureConfig:
    dhcp_most_common_servers = dhcp_analyzer.most_common_servers()
    dhcp_config = FigureConfig(
        "Most Common Servers",
        dhcp_most_common_servers,
        "Server",
        "Count",
        "tab:orange")
    return dhcp_config


def configure_dhcp_most_common_domains(dhcp_analyzer: DHCPAnalyzer) -> FigureConfig:
    dhcp_most_common_domains = dhcp_analyzer.most_common_domains()
    dhcp_config = FigureConfig(
        "Most Common Domains",
        dhcp_most_common_domains,
        "Domain",
        "Count",
        "tab:purple")
    return dhcp_config


def configure_protocol_distribution(base_analyzer: BaseAnalyzer) -> dict:
    protocol_distribution = base_analyzer.protocol_distribution()
    app_config = FigureConfig(
        "Application", protocol_distribution[LayerLevel.APPLICATION], None, None, None)
    transport_config = FigureConfig(
        "Transport", protocol_distribution[LayerLevel.TRANSPORT], None, None, None)
    network_config = FigureConfig(
        "Network", protocol_distribution[LayerLevel.NETWORK], None, None, None)
    link_config = FigureConfig("Link", protocol_distribution[LayerLevel.LINK], None, None, None)
    return {
        LayerLevel.APPLICATION: app_config,
        LayerLevel.TRANSPORT: transport_config,
        LayerLevel.NETWORK: network_config,
        LayerLevel.LINK: link_config
    }


def analyze_pcap(ctx: Context) -> dict:

    # Prepare analyzers
    base_analyzer = BaseAnalyzer(ctx.get_df())
    dns_analyzer = DNSAnalyzer(ctx.get_df())
    dhcp_analyzer = DHCPAnalyzer(ctx.get_df())

    # Analyze
    start_time, end_time, duration = base_analyzer.time_range_and_duration()

    speed_config = configure_speed_graph(base_analyzer)
    dns_domains = configure_dns_most_queried_domains(dns_analyzer)
    dns_servers = configure_dns_most_common_servers(dns_analyzer)
    dhcp_clients = configure_dhcp_most_common_clients(dhcp_analyzer)
    dhcp_servers = configure_dhcp_most_common_servers(dhcp_analyzer)
    dhcp_domains = configure_dhcp_most_common_domains(dhcp_analyzer)
    protocol_distribution = configure_protocol_distribution(base_analyzer)
    indicators = {
        "packet_count": base_analyzer.packet_count(),
        "data_amount": base_analyzer.total_size(),
        "duration": duration.total_seconds(),
        "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
    }

    return {
        "dns_domains": dns_domains,
        "dns_servers": dns_servers,
        "speed_config": speed_config,
        "indicators": indicators,
        "dhcp_clients": dhcp_clients,
        "dhcp_servers": dhcp_servers,
        "dhcp_domains": dhcp_domains,
        "protocol_distribution": protocol_distribution
    }


if __name__ == '__main__':
    context = Context()
    ui.start_app(context, analyze_pcap)
