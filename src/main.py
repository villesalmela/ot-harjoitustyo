import json
from collections import Counter
from datetime import datetime

from scapy.packet import Packet
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.l2 import Ether, ARP
from scapy.layers.dns import DNS
# from scapy.layers.http import HTTPRequest, HTTPResponse
# from scapy.layers.tls.handshake import TLSServerHello, TLSClientHello
# from scapy.layers.dhcp import DHCP
from scapy.utils import rdpcap
import tldextract

from packet import Packet as myPacket
from layer_type import LayerType
from layer import Layer
from layers.ethernet import Ethernet as myEthernet
from layers.ip import IP as myIP
from layers.tcp import TCP as myTCP
from layers.udp import UDP as myUDP
from layers.dns import DNS as myDNS
from dns_opcode import DNSOpCode
from dns_qtype import DNSQType
from dns_dir import DNSDir
from ui.ui import start_app


def parse_dns_answers(dns_layer) -> list[dict[str, str | int]]:
    """Generated with ChatGPT.

    Parse DNS answers from a Scapy DNS layer object to extract answer fields and their values in a
    dictionary.

    :param dns_layer: Scapy DNS response object
    :return: dictionary containing answer fields and their values
    """
    answers = []
    answer_rr = dns_layer.an  # Start with the first answer in the response
    while answer_rr:
        answers.append(answer_rr.fields.copy())
        answer_rr = answer_rr.payload  # Move to the next answer, if any
        if not answer_rr:  # Stop if no more answers
            break
    for answer in answers:
        for key, value in answer.items():
            answer[key] = value
    return answers


def parse_ether(ether_layer: Ether) -> tuple[myEthernet, int, int]:
    return myEthernet(ether_layer.src, ether_layer.dst), len(ether_layer), len(ether_layer.payload)


def parse_ip(ip_layer: IP) -> tuple[myIP, int, int]:
    return myIP(ip_layer.src, ip_layer.dst), len(ip_layer), len(ip_layer.payload)


def parse_tcp(tcp_layer: TCP) -> tuple[myTCP, int, int]:
    return myTCP(tcp_layer.sport, tcp_layer.dport), len(tcp_layer), len(tcp_layer.payload)


def parse_udp(udp_layer: UDP) -> tuple[myUDP, int, int]:
    return myUDP(udp_layer.sport, udp_layer.dport), len(udp_layer), len(udp_layer.payload)


def parse_dns(dns_layer: DNS) -> tuple[myDNS, int, int]:
    if DNSDir(dns_layer.qr) == DNSDir.RESPONSE:
        answers = parse_dns_answers(dns_layer)
    else:
        answers = None
    return myDNS(
        DNSDir(dns_layer.qr), DNSOpCode(dns_layer.opcode),
        DNSQType(dns_layer.qd.qtype),
        dns_layer.qd.qname,
        answers
    ), len(dns_layer), len(dns_layer.payload)

def parse_link(packet: Packet) -> Layer | None:
    if Ether in packet:
        return Layer(*parse_ether(packet[Ether]))
    
def parse_network(packet: Packet) -> Layer | None:
    if IP in packet:
        return Layer(*parse_ip(packet[IP]))
    
def parse_transport(packet: Packet) -> Layer | None:
    if TCP in packet:
        return Layer(*parse_tcp(packet[TCP]))
    elif UDP in packet:
        return Layer(*parse_udp(packet[UDP]))
    
def parse_application(packet: Packet) -> Layer | None:
    if DNS in packet:
        return Layer(*parse_dns(packet[DNS]))

def parse_pcap(pcap_file: str) -> list[myPacket]:
    packets = rdpcap(pcap_file)
    parsed_packets = []

    for packet in packets:

        current_packet = myPacket(datetime.fromtimestamp(float(packet.time)), len(packet))
        current_packet.layers[LayerType.LINK] = parse_link(packet)
        current_packet.layers[LayerType.NETWORK] = parse_network(packet)
        current_packet.layers[LayerType.TRANSPORT] = parse_transport(packet)
        current_packet.layers[LayerType.APPLICATION] = parse_application(packet)
        
        parsed_packets.append(current_packet)

    return parsed_packets


def extract_2ld(fqdn):
    """Generated with ChatGPT.

    Extract the second level domain from a fully qualified domain name (FQDN).
    :param fqdn: Fully qualified domain name
    :return: 2LD and TLD combined
    """

    if not fqdn:
        raise ValueError("FQDN is empty")

    # First try with tldextract
    extracted = tldextract.extract(fqdn)
    if extracted.domain and extracted.suffix:
        # If both parts are identified, return them
        return f"{extracted.domain}.{extracted.suffix}"

    # Fallback mechanism
    parts = fqdn.split('.')

    # Basic assumption: The last two parts are the domain and TLD
    if len(parts) >= 2:
        return f"{parts[-2]}.{parts[-1]}"
    
    # Return the original
    return fqdn


def count_dns_domains(packets: list[myPacket]) -> dict[str, int]:
    """Return a counter object containing number of queries per domain name."""
    counter = Counter()
    for packet in packets:
        dns_layer = packet.layers[LayerType.APPLICATION]
        if dns_layer and dns_layer.name == "DNS" and dns_layer.data["direction"] == DNSDir.QUERY:
            fqdn = dns_layer.data["name"].strip(".")
            domain = extract_2ld(fqdn)
            counter[domain] += 1
    return dict(counter)


def analyze_pcap(filename: str) -> tuple[str, dict[str, int]]:
    out = ""
    # Parse the PCAP file
    parsed_packets = parse_pcap(filename)

    # Display the parsed packets
    for packet in parsed_packets:
        out += str(packet) + "\n"

    # Summary
    out += "\n### SUMMARY ###\n"
    out += f"Total packets: {len(parsed_packets)}\n"
    dns_stats = count_dns_domains(parsed_packets)
    out += f"Count of DNS queries by FQDN: {json.dumps(dns_stats, indent=4)}"

    return out, dns_stats


if __name__ == '__main__':
    start_app(analyze_pcap)
