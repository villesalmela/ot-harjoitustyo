import pandas as pd

from packet_parser.pcap_parser import PcapParser
from analyzer.dns_analyzer import DNSAnalyzer
from analyzer.dhcp_analyzer import DHCPAnalyzer
from analyzer.base_analyzer import BaseAnalyzer
from ui import ui
from ui.figure_config import FigureConfig
from utils.utils import scale_bits, convert_to_bits
from components.packet import Packet as myPacket



class Context:
    def __init__(self) -> None:
        self.details = ""
        self.df = pd.DataFrame()

    def get_df(self):
        return self.df.copy()

    def reset(self):
        self.details = ""
        self.df = pd.DataFrame()

    def append(self, packets: list[myPacket]):
        df = pd.DataFrame([packet.flatten() for packet in packets]).set_index("packet.uid")
        self.df = pd.concat([self.df, df])

        # for debugging
        # pd.set_option('display.max_columns', None)
        # pd.set_option('display.width', 300)
        # print(self.df)


def configure_speed_graph(base_analyzer: BaseAnalyzer) -> FigureConfig:
    # Get the time series data
    bytes_per_second, max_bytes_per_second = base_analyzer.time_series(100)

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


def analyze_pcap(ctx: Context) -> tuple[str | FigureConfig | dict, ...]:

    # Prepare analyzers
    base_analyzer = BaseAnalyzer(ctx.get_df())
    dns_analyzer = DNSAnalyzer(ctx.get_df())
    dhcp_analyzer = DHCPAnalyzer(ctx.get_df())

    # Analyze
    start_time, end_time, duration = base_analyzer.time_range_and_duration()

    speed_config = configure_speed_graph(base_analyzer)
    dns1_config = configure_dns_most_queried_domains(dns_analyzer)
    dns2_config = configure_dns_most_common_servers(dns_analyzer)
    dhcp1_config = configure_dhcp_most_common_clients(dhcp_analyzer)
    dhcp2_config = configure_dhcp_most_common_servers(dhcp_analyzer)
    dhcp3_config = configure_dhcp_most_common_domains(dhcp_analyzer)
    indicators = {
        "packet_count": len(ctx.df),
        "data_amount": base_analyzer.total_size(),
        "duration": duration.total_seconds(),
        "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
    }

    return ctx.details, dns1_config, dns2_config, speed_config, indicators, dhcp1_config, \
        dhcp2_config, dhcp3_config


if __name__ == '__main__':
    context = Context()
    ui.start_app(context, analyze_pcap)
