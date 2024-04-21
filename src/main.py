import json

from packet_parser.pcap_parser import PcapParser
from analyzer.dns_analyzer import DNSAnalyzer
from analyzer.dhcp_analyzer import DHCPAnalyzer
from ui import ui
from utils.utils import JSONEncoder


def analyze_pcap(filename: str) -> tuple[str, dict[str, int], dict[str, int]]:
    out = ""
    # Parse the PCAP file
    parser = PcapParser()
    parsed_packets = parser.parse_pcap(filename)

    # Display the parsed packets
    for packet in parsed_packets:
        out += str(packet) + "\n"

    # Summary
    out += "\n### SUMMARY ###\n"
    out += f"Total packets: {len(parsed_packets)}\n"
    dns_analyzer = DNSAnalyzer(parsed_packets)
    dns_most_queried_domains = dns_analyzer.most_queried_domains()
    dns_most_common_servers = dns_analyzer.most_common_servers()
    dhcp_analyzer = DHCPAnalyzer(parsed_packets)
    dhcp_most_common_clients = dhcp_analyzer.most_common_clients()
    dhcp_most_common_clients_str = json.dumps(dhcp_most_common_clients, cls=JSONEncoder, indent=4)
    out += f"Most common DHCP clients: {dhcp_most_common_clients_str}\n"
    out += f"Count of DNS queries by FQDN: {json.dumps(dns_most_queried_domains, indent=4)}\n"
    out += f"Most common DNS servers: {json.dumps(dns_most_common_servers, indent=4)}\n"

    return out, dns_most_queried_domains, dns_most_common_servers


if __name__ == '__main__':
    ui.start_app(analyze_pcap)
