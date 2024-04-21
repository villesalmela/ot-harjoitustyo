from enum import Enum


class DHCPMessageType(Enum):
    "Generated with ChatGPT."
    UNKNOWN = None
    DHCPDISCOVER = 1
    DHCPOFFER = 2
    DHCPREQUEST = 3
    DHCPDECLINE = 4
    DHCPACK = 5
    DHCPNAK = 6
    DHCPRELEASE = 7
    DHCPINFORM = 8

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN
