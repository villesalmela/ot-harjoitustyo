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


class Context:
    """Holds the context of the application and provides methods for interacting with the
    storage backend."""

    def __init__(self, reset_db=False) -> None:
        self.df = pd.DataFrame()
        self.storage = DBStorage(config.DB_PATH, reset=reset_db)

    def __len__(self):
        return len(self.df)

    def get_df(self) -> pd.DataFrame:
        """Get the DataFrame, which holds all the packets.

        The dataframe is the main data structure for the application, holding all the information
        parsed from the analyzed pcap files.

        Returns:
            pd.DataFrame: Pandas DataFrame with packets
        """
        return self.df.copy()

    def reset(self) -> None:
        """Clears the application context.

        Database is left untouched.
        """
        self.df = pd.DataFrame()

    def save(self, name: str) -> None:
        """The current application context is saved to the storage backend.

        Args:
            name (str): name of the save slot
        """
        self.storage.save(self.df, name)

    def load(self, name: str) -> None:
        """Loads the application context from the storage backend.

        Args:
            name (str): name of the save slot
        """
        self.df = self.storage.load(name)

    def list_slots(self) -> list[str]:
        """Lists all available save slots.

        Returns:
            list[str]: list of slot names
        """
        return self.storage.list_slots()

    def del_slot(self, name: str) -> None:
        """Deletes a save slot.

        Args:
            name (str): name of the save slot
        """
        self.storage.del_slot(name)

    def append(self, file_path: str) -> None:
        """Parse the pcap file and append the packets to the application context.

        Args:
            file_path (str): location of the pcap file
        """
        parsed_packets = PcapParser().parse_pcap(file_path)

        flat_packets = []
        for packet in parsed_packets:
            flat_packet = packet.flatten()
            flat_packet.update({"packet.str": str(packet)})
            flat_packets.append(flat_packet)
        df = pd.DataFrame(flat_packets).set_index("packet.uid")
        self.df = pd.concat([self.df, df])
        self.df = DBStorage.adjust_dtypes(self.df)


def _configure_speed_graph(base_analyzer: BaseAnalyzer) -> FigureConfig:
    """Configure the speed graph, given already initialized base analyzer.

    Args:
        base_analyzer (BaseAnalyzer): initialized base analyzer

    Returns:
        FigureConfig: configuration for the speed graph
    """
    bytes_per_second, max_bytes_per_second = base_analyzer.time_series_speed(100)

    bits_per_second = convert_to_bits(bytes_per_second)
    max_bits_per_second = convert_to_bits(max_bytes_per_second)

    scaled_speed_max, unit_max = scale_bits(max_bits_per_second)
    scaled_speed, unit = scale_bits(bits_per_second)

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


def _configure_dns_most_queried_domains(dns_analyzer: DNSAnalyzer) -> FigureConfig:
    """Configure the most queried domains graph, given already initialized DNS analyzer.

    Args:
        dns_analyzer (DNSAnalyzer): initialized DNS analyzer

    Returns:
        FigureConfig: configuration for the most queried domains graph
    """
    dns_most_queried_domains = dns_analyzer.most_queried_domains()
    dns1_config = FigureConfig(
        "Most Queried Domains",
        dns_most_queried_domains,
        "Domain",
        "Count",
        "tab:blue")
    return dns1_config


def _configure_dns_most_common_servers(dns_analyzer: DNSAnalyzer) -> FigureConfig:
    """Configure the most common servers graph, given already initialized DNS analyzer.

    Args:
        dns_analyzer (DNSAnalyzer): initialized DNS analyzer

    Returns:
        FigureConfig: configuration for the most common servers graph
    """
    dns_most_common_servers = dns_analyzer.most_common_servers()
    dns2_config = FigureConfig(
        "Most Common Servers",
        dns_most_common_servers,
        "Server",
        "Count",
        "tab:red")
    return dns2_config


def _configure_dhcp_most_common_clients(dhcp_analyzer: DHCPAnalyzer) -> FigureConfig:
    """Configure the most common clients graph, given already initialized DHCP analyzer.

    Args:
        dhcp_analyzer (DHCPAnalyzer): initialized DHCP analyzer

    Returns:
        FigureConfig: configuration for the most common clients graph
    """
    dhcp_most_common_clients = dhcp_analyzer.most_common_clients()
    dhcp_config = FigureConfig(
        "Most Common Clients",
        dhcp_most_common_clients,
        "Client",
        "Count",
        "tab:green")
    return dhcp_config


def _configure_dhcp_most_common_servers(dhcp_analyzer: DHCPAnalyzer) -> FigureConfig:
    """Configure the most common servers graph, given already initialized DHCP analyzer.

    Args:
        dhcp_analyzer (DHCPAnalyzer): initialized DHCP analyzer

    Returns:
        FigureConfig: configuration for the most common servers graph
    """
    dhcp_most_common_servers = dhcp_analyzer.most_common_servers()
    dhcp_config = FigureConfig(
        "Most Common Servers",
        dhcp_most_common_servers,
        "Server",
        "Count",
        "tab:orange")
    return dhcp_config


def _configure_dhcp_most_common_domains(dhcp_analyzer: DHCPAnalyzer) -> FigureConfig:
    """Configure the most common domains graph, given already initialized DHCP analyzer.

    Args:
        dhcp_analyzer (DHCPAnalyzer): initialized DHCP analyzer

    Returns:
        FigureConfig: configuration for the most common domains graph
    """
    dhcp_most_common_domains = dhcp_analyzer.most_common_domains()
    dhcp_config = FigureConfig(
        "Most Common Domains",
        dhcp_most_common_domains,
        "Domain",
        "Count",
        "tab:purple")
    return dhcp_config


def _configure_protocol_distribution(base_analyzer: BaseAnalyzer) -> dict:
    """Configure the protocol distribution graph, given already initialized base analyzer.

    Args:
        base_analyzer (BaseAnalyzer): initialized base analyzer

    Returns:
        dict: configuration for the protocol distribution graph
    """
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
    """Analyze the pcap file and return the results.

    This method is typically called by the UI every time the application context has been updated.

    Args:
        ctx (Context): application context

    Returns:
        dict: results of the analysis
    """

    base_analyzer = BaseAnalyzer(ctx.get_df())
    dns_analyzer = DNSAnalyzer(ctx.get_df())
    dhcp_analyzer = DHCPAnalyzer(ctx.get_df())

    start_time, end_time, duration = base_analyzer.time_range_and_duration()
    speed_config = _configure_speed_graph(base_analyzer)
    dns_domains = _configure_dns_most_queried_domains(dns_analyzer)
    dns_servers = _configure_dns_most_common_servers(dns_analyzer)
    dhcp_clients = _configure_dhcp_most_common_clients(dhcp_analyzer)
    dhcp_servers = _configure_dhcp_most_common_servers(dhcp_analyzer)
    dhcp_domains = _configure_dhcp_most_common_domains(dhcp_analyzer)
    protocol_distribution = _configure_protocol_distribution(base_analyzer)
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
