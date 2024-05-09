"Convenience module for simplifying parser imports."

from packet_parser.dhcp_parser import DHCPParser
from packet_parser.dns_parser import DNSParser


PARSERS = [
    DHCPParser,
    DNSParser
]
