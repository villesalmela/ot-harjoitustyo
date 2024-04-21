"Generated with ChatGPT."
from enum import Enum


class ICMPType(Enum):
    UNKNOWN = None
    ECHO_REPLY = 0
    DEST_UNREACH = 3
    SOURCE_QUENCH = 4
    REDIRECT = 5
    ECHO_REQUEST = 8
    ROUTER_ADVERTISEMENT = 9
    ROUTER_SOLICITATION = 10
    TIME_EXCEEDED = 11
    PARAMETER_PROBLEM = 12
    TIMESTAMP_REQUEST = 13
    TIMESTAMP_REPLY = 14
    INFORMATION_REQUEST = 15
    INFORMATION_RESPONSE = 16
    ADDRESS_MASK_REQUEST = 17
    ADDRESS_MASK_REPLY = 18
    TRACEROUTE = 30
    DATAGRAM_CONVERSION_ERROR = 31
    MOBILE_HOST_REDIRECT = 32
    IPV6_WHERE_ARE_YOU = 33
    IPV6_I_AM_HERE = 34
    MOBILE_REGISTRATION_REQUEST = 35
    MOBILE_REGISTRATION_REPLY = 36
    DOMAIN_NAME_REQUEST = 37
    DOMAIN_NAME_REPLY = 38
    SKIP = 39
    PHOTURIS = 40
    EXTENDED_ECHO_REQUEST = 42
    EXTENDED_ECHO_REPLY = 43

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


class ICMPCode(Enum):
    UNKNOWN = None
    # No Code
    NO_CODE = 0

    # DEST_UNREACH Codes
    NETWORK_UNREACHABLE = (ICMPType.DEST_UNREACH, 0)
    HOST_UNREACHABLE = (ICMPType.DEST_UNREACH, 1)
    PROTOCOL_UNREACHABLE = (ICMPType.DEST_UNREACH, 2)
    PORT_UNREACHABLE = (ICMPType.DEST_UNREACH, 3)
    FRAGMENTATION_NEEDED = (ICMPType.DEST_UNREACH, 4)
    SOURCE_ROUTE_FAILED = (ICMPType.DEST_UNREACH, 5)
    NETWORK_UNKNOWN = (ICMPType.DEST_UNREACH, 6)
    HOST_UNKNOWN = (ICMPType.DEST_UNREACH, 7)
    NETWORK_PROHIBITED = (ICMPType.DEST_UNREACH, 9)
    HOST_PROHIBITED = (ICMPType.DEST_UNREACH, 10)
    TOS_NETWORK_UNREACHABLE = (ICMPType.DEST_UNREACH, 11)
    TOS_HOST_UNREACHABLE = (ICMPType.DEST_UNREACH, 12)
    COMMUNICATION_PROHIBITED = (ICMPType.DEST_UNREACH, 13)
    HOST_PRECEDENCE_VIOLATION = (ICMPType.DEST_UNREACH, 14)
    PRECEDENCE_CUTOFF = (ICMPType.DEST_UNREACH, 15)

    # REDIRECT Codes
    NETWORK_REDIRECT = (ICMPType.REDIRECT, 0)
    HOST_REDIRECT = (ICMPType.REDIRECT, 1)
    TOS_NETWORK_REDIRECT = (ICMPType.REDIRECT, 2)
    TOS_HOST_REDIRECT = (ICMPType.REDIRECT, 3)

    # TIME_EXCEEDED Codes
    TTL_ZERO_DURING_TRANSIT = (ICMPType.TIME_EXCEEDED, 0)
    TTL_ZERO_DURING_REASSEMBLY = (ICMPType.TIME_EXCEEDED, 1)

    # PARAMETER_PROBLEM Codes
    IP_HEADER_BAD = (ICMPType.PARAMETER_PROBLEM, 0)
    REQUIRED_OPTION_MISSING = (ICMPType.PARAMETER_PROBLEM, 1)

    # PHOTURIS Codes
    BAD_SPI = (ICMPType.PHOTURIS, 0)
    AUTHENTICATION_FAILED = (ICMPType.PHOTURIS, 1)
    DECOMPRESSION_FAILED = (ICMPType.PHOTURIS, 2)
    DECRYPTION_FAILED = (ICMPType.PHOTURIS, 3)
    NEED_AUTHENTICATION = (ICMPType.PHOTURIS, 4)
    NEED_AUTHORIZATION = (ICMPType.PHOTURIS, 5)

    @classmethod
    def _missing_(cls, key):
        if isinstance(key, tuple):
            icmp_type, icmp_code = key
            if icmp_code == 0:
                return cls.NO_CODE
        return cls.UNKNOWN
