from scapy.packet import Packet
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.l2 import Ether, ARP
from scapy.layers.dns import DNS
# from scapy.layers.http import HTTPRequest, HTTPResponse
# from scapy.layers.tls.handshake import TLSServerHello, TLSClientHello
# from scapy.layers.dhcp import DHCP
from scapy.utils import rdpcap
from datetime import datetime
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
from collections import Counter
import json


def parse_dns_answers(dns_layer) -> list[dict[str, str|int]]:
    """
    Generated with ChatGPT
    Parse DNS answers from a Scapy DNS layer object to extract answer fields and their values in a dictionary.
    
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
            answer[key] = value.decode("utf-8") if isinstance(value, bytes) else value
    return answers


def parse_pcap(pcap_file: str) -> list[myPacket]:
    packets = rdpcap(pcap_file)
    parsed_packets = []

    for packet in packets:
        packet: Packet

        current_packet = myPacket(datetime.fromtimestamp(float(packet.time)), len(packet))
        if Ether in packet:
            ether_layer = packet[Ether]
            current_packet.layers[LayerType.LINK] = Layer(myEthernet(ether_layer.src, ether_layer.dst), current_packet, len(ether_layer), len(ether_layer.payload))
            
            if IP in packet:
                ip_layer = packet[IP]
                current_packet.layers[LayerType.NETWORK] = Layer(myIP(ip_layer.src, ip_layer.dst), current_packet, len(ip_layer), len(ip_layer.payload))
                
                if TCP in packet:
                    tcp_layer = packet[TCP]
                    current_packet.layers[LayerType.TRANSPORT] = Layer(myTCP(tcp_layer.sport, tcp_layer.dport), current_packet, len(tcp_layer), len(tcp_layer.payload))
                elif UDP in packet:
                    udp_layer = packet[UDP]
                    current_packet.layers[LayerType.TRANSPORT] = Layer(myUDP(udp_layer.sport, udp_layer.dport), current_packet, len(udp_layer), len(udp_layer.payload))

                if DNS in packet:
                    dns_layer = packet[DNS]
                    if DNSDir(dns_layer.qr) == DNSDir.RESPONSE:
                        answers = parse_dns_answers(dns_layer)
                    else:
                        answers = None
                    current_packet.layers[LayerType.APPLICATION] = Layer(myDNS(DNSDir(dns_layer.qr), DNSOpCode(dns_layer.opcode), DNSQType(dns_layer.qd.qtype), dns_layer.qd.qname.decode("utf-8"), answers), current_packet, len(dns_layer), len(dns_layer.payload))
                    parsed_packets.append(current_packet)

    return parsed_packets


def extract_main_part_with_fallback(fqdn):
    # First try with tldextract
    extracted = tldextract.extract(fqdn)
    if extracted.domain and extracted.suffix:
        # If both parts are identified, return them
        return f"{extracted.domain}.{extracted.suffix}"

    # Fallback mechanism
    parts = fqdn.split('.')
    # Basic assumption: The last two parts are the domain and TLD
    # This might not be perfect but works as a simple heuristic
    if len(parts) >= 2:
        return f"{parts[-2]}.{parts[-1]}"
    if len(parts) == 1:
        # Edge case: only one part is present
        return parts[0]

    # If somehow we have an unexpected format, return the input
    return fqdn


def count_dns_domains(packets: list[myPacket]) -> dict[str, int]:
    """Return a counter object containing number of queries per domain name."""
    counter = Counter()
    for packet in packets:
        dns_layer = packet.layers[LayerType.APPLICATION]
        if dns_layer and dns_layer.name == "DNS" and dns_layer.data["direction"] == DNSDir.QUERY:
            fqdn = dns_layer.data["name"].strip(".")
            domain = extract_main_part_with_fallback(fqdn)
            counter[domain] += 1
    return dict(counter)


if __name__ == "__main__":  

    # Load the PCAP file
    pcap_file = "assets/dns.pcap"

    # Parse the PCAP file
    parsed_packets = parse_pcap(pcap_file)
    
    # Display the parsed packets
    for packet in parsed_packets:
        print(packet)

    # Summary
    print("\n### SUMMARY ###")
    print(f"Total packets: {len(parsed_packets)}")
    print(f"Count of DNS queries by FQDN: {json.dumps(count_dns_domains(parsed_packets), indent=4)}")
        

    
    

