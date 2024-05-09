"Convenience module for simplifying layer imports."

from layers.arp import ARP
from layers.dhcp import DHCP
from layers.dns import DNS
from layers.ethernet import Ethernet
from layers.icmp import ICMP
from layers.ip import IP
from layers.sll import SLL
from layers.udp import UDP
from layers.tcp import TCP
from layers.raw import RAW


LAYERS = [
    ARP,
    DHCP,
    DNS,
    Ethernet,
    ICMP,
    IP,
    SLL,
    UDP,
    TCP,
    RAW
]
