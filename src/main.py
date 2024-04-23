import json

from packet_parser.pcap_parser import PcapParser
from analyzer.dns_analyzer import DNSAnalyzer
from analyzer.dhcp_analyzer import DHCPAnalyzer
from analyzer.base_analyzer import BaseAnalyzer
from ui import ui
from ui.figure_config import FigureConfig
from utils.utils import JSONEncoder, scale_bits, convert_to_bits


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


def analyze_pcap(filename: str) -> tuple[str | FigureConfig | dict, ...]:
    out = ""

    # Parse the PCAP file
    parsed_packets = PcapParser().parse_pcap(filename)

    # Display the parsed packets
    for packet in parsed_packets:
        out += str(packet) + "\n"

    # Prepare analyzers
    base_analyzer = BaseAnalyzer(parsed_packets)
    dns_analyzer = DNSAnalyzer(parsed_packets)
    dhcp_analyzer = DHCPAnalyzer(parsed_packets)

    # Analyze
    dhcp_most_common_clients = dhcp_analyzer.most_common_clients()
    start_time, end_time, duration = base_analyzer.time_range_and_duration()

    # Summary
    out += (
        f"\n### SUMMARY ###\nTotal packets: {len(parsed_packets)}\nMost common DHCP clients: "
        f"{json.dumps(dhcp_most_common_clients, cls=JSONEncoder, indent=4)}")

    speed_config = configure_speed_graph(base_analyzer)
    dns1_config = configure_dns_most_queried_domains(dns_analyzer)
    dns2_config = configure_dns_most_common_servers(dns_analyzer)
    indicators = {
        "packet_count": len(parsed_packets),
        "data_amount": base_analyzer.total_size(),
        "duration": duration.total_seconds(),
        "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
    }

    return out, dns1_config, dns2_config, speed_config, indicators


if __name__ == '__main__':
    ui.start_app(analyze_pcap)
