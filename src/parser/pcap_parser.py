from datetime import datetime

from scapy.packet import Packet
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.l2 import Ether, ARP
from scapy.layers.dns import DNS
# from scapy.layers.http import HTTPRequest, HTTPResponse
# from scapy.layers.tls.handshake import TLSServerHello, TLSClientHello
from scapy.layers.dhcp import DHCP, BOOTP
from scapy.utils import rdpcap

from components.packet import Packet as myPacket
from layers.layer_level import LayerLevel
from components.layer import Layer
from layers.ethernet import Ethernet as myEthernet
from layers.ip import IP as myIP
from layers.tcp import TCP as myTCP
from layers.udp import UDP as myUDP
from parser.dns_parser import DNSParser
from parser.dhcp_parser import DHCPParser


class PcapParser:

    def __init__(self) -> None:
        self.raw_packets = []
        self.parsed_packets = []


    def parse_pcap(self, filename: str) -> list[myPacket]:
        raw_packets = rdpcap(filename)
        parsed_packets = []

        for packet in raw_packets:

            parsed_packet = myPacket(datetime.fromtimestamp(float(packet.time)), len(packet))
            parsed_packet.layers[LayerLevel.LINK] = self.parse_link(packet)
            parsed_packet.layers[LayerLevel.NETWORK] = self.parse_network(packet)
            parsed_packet.layers[LayerLevel.TRANSPORT] = self.parse_transport(packet)
            parsed_packet.layers[LayerLevel.APPLICATION] = self.parse_application(packet)

            parsed_packets.append(parsed_packet)

        self.raw_packets.extend(raw_packets)
        self.parsed_packets.extend(parsed_packets)

        return parsed_packets


    @staticmethod
    def parse_ether(ether_layer: Ether) -> tuple[myEthernet, int, int]:
        return myEthernet(ether_layer.src, ether_layer.dst), len(ether_layer), len(ether_layer.payload)


    @staticmethod
    def parse_ip(ip_layer: IP) -> tuple[myIP, int, int]:
        return myIP(ip_layer.src, ip_layer.dst), len(ip_layer), len(ip_layer.payload)


    @staticmethod
    def parse_tcp(tcp_layer: TCP) -> tuple[myTCP, int, int]:
        return myTCP(tcp_layer.sport, tcp_layer.dport), len(tcp_layer), len(tcp_layer.payload)


    @staticmethod
    def parse_udp(udp_layer: UDP) -> tuple[myUDP, int, int]:
        return myUDP(udp_layer.sport, udp_layer.dport), len(udp_layer), len(udp_layer.payload)


    @classmethod
    def parse_link(cls, packet: Packet) -> Layer | None:
        if Ether in packet:
            return Layer(*cls.parse_ether(packet[Ether]))
        return None


    @classmethod
    def parse_network(cls, packet: Packet) -> Layer | None:
        if IP in packet:
            return Layer(*cls.parse_ip(packet[IP]))
        return None


    @classmethod
    def parse_transport(cls, packet: Packet) -> Layer | None:
        if TCP in packet:
            return Layer(*cls.parse_tcp(packet[TCP]))
        if UDP in packet:
            return Layer(*cls.parse_udp(packet[UDP]))
        return None


    @staticmethod
    def parse_application(packet: Packet) -> Layer | None:
        if DNS in packet:
            return Layer(*DNSParser.parse_dns(packet[DNS]))
        if DHCP in packet and BOOTP in packet:
            dhcp_layer = packet[DHCP]
            bootp_layer = packet[BOOTP]
            return Layer(*DHCPParser.parse_dhcp(bootp_layer, dhcp_layer))
        return None
