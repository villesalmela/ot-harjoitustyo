from datetime import datetime
from pathlib import Path

from scapy.utils import rdpcap
from scapy.packet import Packet, Raw, NoPayload
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.inet6 import IPv6, _ICMPv6, _ICMPv6NDGuessPayload
from scapy.layers.l2 import Ether, ARP, CookedLinux, ETHER_TYPES
from scapy.layers.dns import DNS
from scapy.layers.dhcp import DHCP, BOOTP
# from scapy.layers.http import HTTPRequest, HTTPResponse
# from scapy.layers.tls.handshake import TLSServerHello, TLSClientHello

from components.packet import Packet as myPacket
from components.layer import Layer
from layers.layer_level import LayerLevel
from layers.ethernet import Ethernet as myEthernet
from layers.sll import SLL as mySLL, CookedPacketType
from layers.ip import IP as myIP, IPVersion
from layers.icmp import ICMP as myICMP, ICMPVersion, ICMPCode, ICMPType, ICMPv6Code, ICMPv6Type
from layers.tcp import TCP as myTCP
from layers.udp import UDP as myUDP
from layers.arp import ARP as myARP, ARPOpCode, HardwareType
from layers.raw import RAW as myRaw
from packet_parser.dns_parser import DNSParser
from packet_parser.dhcp_parser import DHCPParser
from utils.utils import convert_mac


class ParsingError(Exception):
    """Failed to parse a packet."""

    def __init__(self, packet_number: int, layer_level: str, packet: Packet) -> None:
        """Initialize ParsingError exception.

        Args:
            packet_number (int): Number of the packet that caused the error
            layer_level (str): Layer level where the error occurred
            packet (Packet): The packet that caused the error
        """

        message = f"Packet {packet_number} on {layer_level.upper()}: Parsing error"
        super().__init__(message)
        self.packet = packet
        self.verbose = True

    def __str__(self):
        if self.verbose:
            details = f"\n{self.packet.show(dump=True)}"
        else:
            details = ""
        return f"{super().__str__()} caused by: {self.__cause__}{details}"


class UnsupportedLayerError(Exception):
    """Unsupported layer in a packet."""

    def __init__(self, layer: Packet) -> None:
        """Initialize UnsupportedLayerError exception.

        Args:
            layer (Packet): The unsupported layer
        """
        super().__init__(f"Unsupported layer: {layer.name}")
        self.packet = layer


class PcapParser:
    """Parses pcap files into custom packets."""

    def __init__(self) -> None:
        self.raw_packets = []
        self.parsed_packets = []
        self.checksum_log = ""
        self.error_log = ""
        self.support_log = ""
        Path("logs").mkdir(parents=True, exist_ok=True)

    def verify_checksum(self, packet_number: int, layer) -> bool:
        """Verify checksum of a layer.

        Logs a message if checksum verification fails.

        Args:
            packet_number (int): Number of the packet
            layer: a Scapy layer object

        Returns:
            bool: True if checksum is valid, False otherwise
        """

        if hasattr(layer, "chksum"):
            checksum_attribute = "chksum"
        elif hasattr(layer, "cksum"):
            checksum_attribute = "cksum"
        else:
            return False

        original_checksum = getattr(layer, checksum_attribute)
        delattr(layer, checksum_attribute)
        if not getattr(layer.__class__(bytes(layer)), checksum_attribute) == original_checksum:
            msg = f"Packet {packet_number}: Checksum verification failed for {layer.summary()}\n"
            self.checksum_log += msg
            return False
        return True

    def parse_pcap(self, filename: str) -> list[myPacket]:
        """Parse pcap file into custom packets.

        Args:
            filename (str): path to the pcap file

        Returns:
            list[myPacket]: list of custom packets
        """

        self.raw_packets = rdpcap(filename)
        for packet_number, packet in enumerate(self.raw_packets, start=1):

            parsed_packet = myPacket(
                datetime.fromtimestamp(
                    float(
                        packet.time)),
                len(packet),
                packet_number)

            for layer_level, layer_parser in [
                (LayerLevel.LINK, self.parse_link),
                (LayerLevel.NETWORK, self.parse_network),
                (LayerLevel.TRANSPORT, self.parse_transport),
                (LayerLevel.APPLICATION, self.parse_application)
            ]:
                try:
                    layer = layer_parser(packet_number, packet)
                    parsed_packet.layers[layer_level] = layer
                except ParsingError as e:
                    parsed_packet.layers[layer_level] = Layer(
                        myRaw(layer_level), len(packet), len(
                            packet.payload))
                    if isinstance(e.__cause__, UnsupportedLayerError):
                        e.verbose = False
                        self.support_log += f"{e}\n"
                        self.support_log += f"PAYLOAD: {e.packet.payload.show(dump=True)}\n"
                    else:
                        self.error_log += f"{e}\n"
                finally:
                    packet = packet.payload
            self.parsed_packets.append(parsed_packet)

        Path("logs/support.log").write_text(self.support_log, encoding="utf-8")
        Path("logs/checksum.log").write_text(self.checksum_log, encoding="utf-8")
        Path("logs/error.log").write_text(self.error_log, encoding="utf-8")
        return self.parsed_packets

    def parse_ether(self, ether_layer: Ether) -> tuple[myEthernet, int, int]:
        """Parse an Ethernet layer.

        Args:
            ether_layer (Ether): Scapy Ethernet layer

        Returns:
            tuple[myEthernet, int, int]: parsed Ethernet layer, total size, payload size in bytes
        """
        return myEthernet(
            ether_layer.src, ether_layer.dst), len(ether_layer), len(
            ether_layer.payload)

    def parse_sll(self, sll_layer: CookedLinux) -> tuple[mySLL, int, int]:
        """Parse a Linux cooked capture layer.

        Args:
            sll_layer (CookedLinux): Scapy Linux cooked capture layer

        Returns:
            tuple[mySLL, int, int]: parsed SLL layer, total size, payload size in bytes
        """
        packet_type = CookedPacketType(sll_layer.pkttype)
        protocol_type: str = ETHER_TYPES[sll_layer.proto]
        src_addr = convert_mac(sll_layer.src)
        return mySLL(src_addr, packet_type, protocol_type), len(sll_layer), len(sll_layer.payload)

    def parse_ip(self, packet_number: int, ip_layer: IP | IPv6) -> tuple[myIP, int, int]:
        """Parse an IP layer.

        Args:
            packet_number (int): Number of the packet
            ip_layer (IP | IPv6): Scapy IP or IPv6 layer

        Raises:
            ValueError: Unsupported IP version

        Returns:
            tuple[myIP, int, int]: parsed IP layer, total size, payload size in bytes
        """
        if isinstance(ip_layer, IP):
            version = IPVersion.IPV4
            checksum_valid = self.verify_checksum(packet_number, ip_layer)
        elif isinstance(ip_layer, IPv6):
            version = IPVersion.IPV6
            checksum_valid = None
        else:
            raise ValueError("Unsupported IP version")
        return myIP(
            version, ip_layer.src, ip_layer.dst, checksum_valid), len(ip_layer), len(
            ip_layer.payload)

    def parse_arp(self, arp_layer: ARP) -> tuple[myARP, int, int]:
        """Parse an ARP layer.

        Args:
            arp_layer (ARP): Scapy ARP layer

        Returns:
            tuple[myARP, int, int]: parsed ARP layer, total size, payload size in bytes
        """
        hwtype = HardwareType(arp_layer.hwtype)
        opcode = ARPOpCode(arp_layer.op)
        hwsrc = arp_layer.hwsrc
        hwdst = arp_layer.hwdst
        psrc = arp_layer.psrc
        pdst = arp_layer.pdst
        return myARP(hwtype, opcode, hwsrc, hwdst, psrc, pdst), len(
            arp_layer), len(arp_layer.payload)

    def parse_tcp(self, packet_number: int, tcp_layer: TCP) -> tuple[myTCP, int, int]:
        """Parse a TCP layer.

        Args:
            packet_number (int): Number of the packet
            tcp_layer (TCP): Scapy TCP layer

        Returns:
            tuple[myTCP, int, int]: parsed TCP layer, total size, payload size in bytes
        """
        checksum_valid = self.verify_checksum(packet_number, tcp_layer)
        return myTCP(
            tcp_layer.sport, tcp_layer.dport, checksum_valid), len(tcp_layer), len(
            tcp_layer.payload)

    def parse_udp(self, packet_number: int, udp_layer: UDP) -> tuple[myUDP, int, int]:
        """Parse a UDP layer.

        Args:
            packet_number (int): Number of the packet
            udp_layer (UDP): Scapy UDP layer

        Returns:
            tuple[myUDP, int, int]: parsed UDP layer, total size, payload size in bytes
        """
        checksum_valid = self.verify_checksum(packet_number, udp_layer)
        return myUDP(
            udp_layer.sport, udp_layer.dport, checksum_valid), len(udp_layer), len(
            udp_layer.payload)

    def parse_icmp(self, packet_number: int, icmp_layer: ICMP) -> tuple[myICMP, int, int]:
        """Parse an ICMP layer.

        Args:
            packet_number (int): Number of the packet
            icmp_layer (ICMP): Scapy ICMP layer

        Returns:
            tuple[myICMP, int, int]: parsed ICMP layer, total size, payload size in bytes
        """
        icmp_type = ICMPType(icmp_layer.type)
        icmp_code = ICMPCode((icmp_type, icmp_layer.code))
        identifier = getattr(icmp_layer, "id", None)
        seq = getattr(icmp_layer, "seq", None)
        checksum_valid = self.verify_checksum(packet_number, icmp_layer)
        return myICMP(ICMPVersion.ICMPV4, icmp_type, icmp_code, None, None, seq, identifier,
                      checksum_valid), len(icmp_layer), len(icmp_layer.payload)

    def parse_icmpv6(self, packet_number: int, packet: Packet) -> tuple[myICMP, int, int]:
        """Parse an ICMPv6 layer.

        Args:
            packet_number (int): Number of the packet
            packet (Packet): Scapy ICMPv6 packet

        Returns:
            tuple[myICMP, int, int]: parsed ICMPv6 layer, total size, payload size in bytes
        """
        for layer in packet:
            if isinstance(layer, (_ICMPv6, _ICMPv6NDGuessPayload)):
                icmp_layer = layer
                break
        icmp_type = ICMPv6Type(icmp_layer.type)
        icmp_code = ICMPv6Code((icmp_type, getattr(icmp_layer, "code", None)))
        identifier = getattr(icmp_layer, "id", None)
        seq = getattr(icmp_layer, "seq", None)
        checksum_valid = self.verify_checksum(packet_number, icmp_layer)
        return myICMP(ICMPVersion.ICMPV6, None, None, icmp_type, icmp_code, seq, identifier,
                      checksum_valid), len(icmp_layer), len(icmp_layer.payload)

    def parse_link(self, packet_number: int, packet: Packet) -> Layer:
        """Parse a link layer.

        Args:
            packet_number (int): Number of the packet
            packet (Packet): Scapy packet

        Raises:
            UnsupportedLayerError: Unsupported layer in the packet
            ParsingError: Failed to parse the packet

        Returns:
            Layer: parsed link layer
        """
        try:
            if Ether in packet:
                return Layer(*self.parse_ether(packet[Ether]))
            if CookedLinux in packet:
                return Layer(*self.parse_sll(packet[CookedLinux]))
            if isinstance(packet, (Raw, NoPayload, type(None))):
                return Layer(myRaw(LayerLevel.LINK), len(packet), len(packet.payload))
            raise UnsupportedLayerError(packet)
        except Exception as e:
            raise ParsingError(packet_number, "link", packet) from e

    def parse_network(self, packet_number: int, packet: Packet) -> Layer:
        """Parse a network layer.

        Args:
            packet_number (int): Number of the packet
            packet (Packet): Scapy packet

        Raises:
            UnsupportedLayerError: Unsupported layer in the packet
            ParsingError: Failed to parse the packet

        Returns:
            Layer: parsed network layer
        """
        try:
            if IP in packet:
                return Layer(*self.parse_ip(packet_number, packet[IP]))
            if IPv6 in packet:
                return Layer(*self.parse_ip(packet_number, packet[IPv6]))
            if ARP in packet:
                return Layer(*self.parse_arp(packet[ARP]))
            if isinstance(packet, (Raw, NoPayload, type(None))):
                return Layer(myRaw(LayerLevel.NETWORK), len(packet), len(packet.payload))
            raise UnsupportedLayerError(packet)
        except Exception as e:
            raise ParsingError(packet_number, "network", packet) from e

    def parse_transport(self, packet_number: int, packet: Packet) -> Layer:
        """Parse a transport layer.

        Args:
            packet_number (int): Number of the packet
            packet (Packet): Scapy packet

        Raises:
            UnsupportedLayerError: Unsupported layer in the packet
            ParsingError: Failed to parse the packet

        Returns:
            Layer: parsed transport layer
        """
        try:
            if TCP in packet:
                return Layer(*self.parse_tcp(packet_number, packet[TCP]))
            if UDP in packet:
                return Layer(*self.parse_udp(packet_number, packet[UDP]))
            if ICMP in packet:
                return Layer(*self.parse_icmp(packet_number, packet[ICMP]))
            if any(isinstance(layer, (_ICMPv6, _ICMPv6NDGuessPayload)) for layer in packet):
                return Layer(*self.parse_icmpv6(packet_number, packet))
            if isinstance(packet, (Raw, NoPayload, type(None))):
                return Layer(myRaw(LayerLevel.TRANSPORT), len(packet), len(packet.payload))
            raise UnsupportedLayerError(packet)
        except Exception as e:
            raise ParsingError(packet_number, "transport", packet) from e

    def parse_application(self, packet_number: int, packet: Packet) -> Layer:
        """Parse an application layer.

        Args:
            packet_number (int): Number of the packet
            packet (Packet): Scapy packet

        Raises:
            UnsupportedLayerError: Unsupported layer in the packet
            ParsingError: Failed to parse the packet

        Returns:
            Layer: parsed application layer
        """
        try:
            if DNS in packet:
                return Layer(*DNSParser.parse_dns(packet[DNS]))
            if DHCP in packet and BOOTP in packet:
                dhcp_layer = packet[DHCP]
                bootp_layer = packet[BOOTP]
                return Layer(*DHCPParser.parse_dhcp(bootp_layer, dhcp_layer))
            if isinstance(packet, (Raw, NoPayload, type(None))):
                return Layer(myRaw(LayerLevel.APPLICATION), len(packet), len(packet.payload))
            raise UnsupportedLayerError(packet)
        except Exception as e:
            raise ParsingError(packet_number, "application", packet) from e
