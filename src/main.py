import json

from packet_parser.pcap_parser import PcapParser
from analyzer.dns_analyzer import DNSAnalyzer
from ui import ui


def analyze_pcap(filename: str) -> tuple[str, dict[str, int]]:
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
    dns_stats = DNSAnalyzer.count_dns_domains(parsed_packets)
    out += f"Count of DNS queries by FQDN: {json.dumps(dns_stats, indent=4)}"

    return out, dns_stats


if __name__ == '__main__':
    ui.start_app(analyze_pcap)
