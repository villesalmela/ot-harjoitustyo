"Convenience module for simplifying property imports."

from layers.arp import ARPOpCode, HardwareType
from layers.dhcp import DHCPMessageType, BOOTPOpCode
from layers.dns import DNSDir, DNSOpCode, DNSQType, DNSRCode
from layers.icmp import ICMPv6Type, ICMPv6Code, ICMPType, ICMPCode, ICMPVersion
from layers.ip import IPVersion
from layers.sll import CookedPacketType


PROPERTIES = [
    ARPOpCode,
    HardwareType,
    DHCPMessageType,
    BOOTPOpCode,
    DNSDir,
    DNSOpCode,
    DNSQType,
    DNSRCode,
    ICMPv6Type,
    ICMPv6Code,
    ICMPType,
    ICMPCode,
    ICMPVersion,
    IPVersion,
    CookedPacketType
]
