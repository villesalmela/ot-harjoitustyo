from typing import Any

from layers.layer_config import LayerConfig
from layers.layer_level import LayerLevel
from components.enum_property import EnumProperty


class ICMPVersion(EnumProperty):
    """Property of ICMP layer, holding the version number.

    Will not raise ValueError if called with invalid value, returns None instead."""
    ICMPV4 = 4
    ICMPV6 = 6


class ICMPType(EnumProperty):
    """Property of ICMP layer, holding Type number for v4.

    Will not raise ValueError if called with invalid value, returns None instead.
    Generated with ChatGPT."""
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


class ICMPCode(EnumProperty):
    """Property of ICMP layer, holding Code number for v4.

    Will not raise ValueError if called with invalid value, returns None instead.
    Generated with ChatGPT."""

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
    def _missing_(cls, value):
        if isinstance(value, tuple):
            _, icmp_code = value
            if icmp_code == 0:
                return cls.NO_CODE
        return cls.UNKNOWN  # defined during subclassing


class ICMPv6Type(EnumProperty):
    """Property of ICMP layer, holding Type number for v6.

    Will not raise ValueError if called with invalid value, returns None instead.
    Generated with ChatGPT."""
    DESTINATION_UNREACHABLE = 1
    PACKET_TOO_BIG = 2
    TIME_EXCEEDED = 3
    PARAMETER_PROBLEM = 4
    PRIVATE_EXPERIMENTATION_1 = 100
    PRIVATE_EXPERIMENTATION_2 = 101
    ECHO_REQUEST = 128
    ECHO_REPLY = 129
    MLD_QUERY = 130
    MLD_REPORT = 131
    MLD_DONE = 132
    ROUTER_SOLICITATION = 133
    ROUTER_ADVERTISEMENT = 134
    NEIGHBOR_SOLICITATION = 135
    NEIGHBOR_ADVERTISEMENT = 136
    REDIRECT_MESSAGE = 137
    ROUTER_RENUMBERING = 138
    ICMP_NODE_INFORMATION_QUERY = 139
    ICMP_NODE_INFORMATION_RESPONSE = 140
    INVERSE_NEIGHBOR_DISCOVERY_SOLICITATION_MESSAGE = 141
    INVERSE_NEIGHBOR_DISCOVERY_ADVERTISEMENT_MESSAGE = 142
    MLD_REPORT_VERSION_2 = 143
    HOME_AGENT_ADDRESS_DISCOVERY_REQUEST_MESSAGE = 144
    HOME_AGENT_ADDRESS_DISCOVERY_REPLY_MESSAGE = 145
    MOBILE_PREFIX_SOLICITATION = 146
    MOBILE_PREFIX_ADVERTISEMENT = 147
    CERTIFICATION_PATH_SOLICITATION = 148
    CERTIFICATION_PATH_ADVERTISEMENT = 149
    MULTICAST_ROUTER_ADVERTISEMENT = 151
    MULTICAST_ROUTER_SOLICITATION = 152
    MULTICAST_ROUTER_TERMINATION = 153
    FMIPV6_MESSAGES = 154
    RPL_CONTROL_MESSAGE = 155
    ILNPV6_LOCATOR_UPDATE_MESSAGE = 156
    DUPLICATE_ADDRESS_REQUEST = 157
    DUPLICATE_ADDRESS_CONFIRMATION = 158
    MPL_CONTROL_MESSAGE = 159
    EXTENDED_ECHO_REQUEST = 160
    EXTENDED_ECHO_REPLY = 161
    PRIVATE_EXPERIMENTATION_3 = 200
    PRIVATE_EXPERIMENTATION_4 = 201


class ICMPv6Code(EnumProperty):
    """Property of ICMP layer, holding Code number for v6.

    Will not raise ValueError if called with invalid value, returns None instead.
    Generated with ChatGPT."""

    # No Code
    NO_CODE = 0

    # DEST_UNREACH Codes
    NO_ROUTE_TO_DESTINATION = (ICMPv6Type.DESTINATION_UNREACHABLE, 0)
    COMMUNICATION_WITH_DEST_PROHIBITED = (ICMPv6Type.DESTINATION_UNREACHABLE, 1)
    BEYOND_SCOPE_OF_SOURCE_ADDRESS = (ICMPv6Type.DESTINATION_UNREACHABLE, 2)
    ADDRESS_UNREACHABLE = (ICMPv6Type.DESTINATION_UNREACHABLE, 3)
    PORT_UNREACHABLE = (ICMPv6Type.DESTINATION_UNREACHABLE, 4)
    SOURCE_ADDRESS_FAILED_INGRESS_EGRESS_POLICY = (ICMPv6Type.DESTINATION_UNREACHABLE, 5)
    REJECT_ROUTE_TO_DESTINATION = (ICMPv6Type.DESTINATION_UNREACHABLE, 6)
    ERROR_IN_SOURCE_ROUTING_HEADER = (ICMPv6Type.DESTINATION_UNREACHABLE, 7)
    HEADERS_TOO_LONG = (ICMPv6Type.DESTINATION_UNREACHABLE, 8)

    # TIME_EXCEEDED Codes
    HOP_LIMIT_EXCEEDED_IN_TRANSIT = (ICMPv6Type.TIME_EXCEEDED, 0)
    FRAGMENT_REASSEMBLY_TIME_EXCEEDED = (ICMPv6Type.TIME_EXCEEDED, 1)

    # PARAMETER_PROBLEM Codes
    ERRONEOUS_HEADER_FIELD_ENCOUNTERED = (ICMPv6Type.PARAMETER_PROBLEM, 0)
    UNRECOGNIZED_NEXT_HEADER_TYPE_ENCOUNTERED = (ICMPv6Type.PARAMETER_PROBLEM, 1)
    UNRECOGNIZED_IPV6_OPTION_ENCOUNTERED = (ICMPv6Type.PARAMETER_PROBLEM, 2)
    IPV6_FIRST_FRAGMENT_HAS_INCOMPLETE_IPV6_HEADER_CHAIN = (ICMPv6Type.PARAMETER_PROBLEM, 3)
    SR_UPPER_LAYER_HEADER_ERROR = (ICMPv6Type.PARAMETER_PROBLEM, 4)
    UNRECOGNIZED_NEXT_HEADER_TYPE_ENCOUNTERED_BY_INTERMEDIATE_NODE = (
        ICMPv6Type.PARAMETER_PROBLEM, 5)
    EXTENSION_HEADER_TOO_BIG = (ICMPv6Type.PARAMETER_PROBLEM, 6)
    EXTENSION_HEADER_CHAIN_TOO_LONG = (ICMPv6Type.PARAMETER_PROBLEM, 7)
    TOO_MANY_EXTENSION_HEADERS = (ICMPv6Type.PARAMETER_PROBLEM, 8)
    TOO_MANY_OPTIONS_IN_EXTENSION_HEADER = (ICMPv6Type.PARAMETER_PROBLEM, 9)
    OPTION_TOO_BIG = (ICMPv6Type.PARAMETER_PROBLEM, 10)

    # ROUTER_RENUMBERING Codes
    ROUTER_RENUMBERING_COMMAND = (ICMPv6Type.ROUTER_RENUMBERING, 0)
    ROUTER_RENUMBERING_RESULT = (ICMPv6Type.ROUTER_RENUMBERING, 1)
    SEQUENCE_NUMBER_RESET = (ICMPv6Type.ROUTER_RENUMBERING, 255)

    # ICMP_NODE_INFORMATION_QUERY Codes
    IPV6_ADDRESS_SUBJECT = (ICMPv6Type.ICMP_NODE_INFORMATION_QUERY, 0)
    NAME_SUBJECT = (ICMPv6Type.ICMP_NODE_INFORMATION_QUERY, 1)
    IPV4_ADDRESS_SUBJECT = (ICMPv6Type.ICMP_NODE_INFORMATION_QUERY, 2)

    # ICMP_NODE_INFORMATION_RESPONSE Codes
    SUCCESSFUL_REPLY = (ICMPv6Type.ICMP_NODE_INFORMATION_RESPONSE, 0)
    REFUSES_TO_SUPPLY_ANSWER = (ICMPv6Type.ICMP_NODE_INFORMATION_RESPONSE, 1)
    QTYPE_UNKNOWN_TO_RESPONDER = (ICMPv6Type.ICMP_NODE_INFORMATION_RESPONSE, 2)

    # Duplicate Address Request Code Suffix
    DAR_MESSAGE = (ICMPv6Type.DUPLICATE_ADDRESS_REQUEST, 0)
    EDAR_MESSAGE_WITH_64_BIT_ROVR_FIELD = (ICMPv6Type.DUPLICATE_ADDRESS_REQUEST, 1)
    EDAR_MESSAGE_WITH_128_BIT_ROVR_FIELD = (ICMPv6Type.DUPLICATE_ADDRESS_REQUEST, 2)
    EDAR_MESSAGE_WITH_192_BIT_ROVR_FIELD = (ICMPv6Type.DUPLICATE_ADDRESS_REQUEST, 3)
    EDAR_MESSAGE_WITH_256_BIT_ROVR_FIELD = (ICMPv6Type.DUPLICATE_ADDRESS_REQUEST, 4)

    # Duplicate Address Confirmation Code Suffix
    DAC_MESSAGE = (ICMPv6Type.DUPLICATE_ADDRESS_CONFIRMATION, 0)
    EDAC_MESSAGE_WITH_64_BIT_ROVR_FIELD = (ICMPv6Type.DUPLICATE_ADDRESS_CONFIRMATION, 1)
    EDAC_MESSAGE_WITH_128_BIT_ROVR_FIELD = (ICMPv6Type.DUPLICATE_ADDRESS_CONFIRMATION, 2)
    EDAC_MESSAGE_WITH_192_BIT_ROVR_FIELD = (ICMPv6Type.DUPLICATE_ADDRESS_CONFIRMATION, 3)
    EDAC_MESSAGE_WITH_256_BIT_ROVR_FIELD = (ICMPv6Type.DUPLICATE_ADDRESS_CONFIRMATION, 4)

    # Extended Echo Request Codes
    EXTENDED_ECHO_REQUEST_NO_ERROR = (ICMPv6Type.EXTENDED_ECHO_REQUEST, 0)

    # Extended Echo Reply Codes
    EXTENDED_ECHO_REPLY_NO_ERROR = (ICMPv6Type.EXTENDED_ECHO_REPLY, 0)
    MALFORMED_QUERY = (ICMPv6Type.EXTENDED_ECHO_REPLY, 1)
    NO_SUCH_INTERFACE = (ICMPv6Type.EXTENDED_ECHO_REPLY, 2)
    NO_SUCH_TABLE_ENTRY = (ICMPv6Type.EXTENDED_ECHO_REPLY, 3)
    MULTIPLE_INTERFACES_SATISFY_QUERY = (ICMPv6Type.EXTENDED_ECHO_REPLY, 4)

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, tuple):
            _, icmp_code = value
            if icmp_code is None or icmp_code == 0:
                return cls.NO_CODE
        return cls.UNKNOWN  # defined during subclassing


class ICMP(LayerConfig):
    """Configuration for ICMP layer."""

    layer_type = LayerLevel.TRANSPORT
    layer_name = "ICMP"
    data: dict[str, Any]
    dtypes = {
        "icmp_type_v4": ICMPType,
        "icmp_code_v4": ICMPCode,
        "icmp_type_v6": ICMPv6Type,
        "icmp_code_v6": ICMPv6Code,
        "version": ICMPVersion
    }

    def __init__(
            self,
            version: ICMPVersion,
            icmp_type: ICMPType | ICMPv6Type,
            icmp_code: ICMPCode | ICMPv6Code,
            seq: int | None,
            identifier: int | None,
            checksum_valid: bool) -> None:
        """Initializes ICMP configuration object with provided details.

        Args:
            version (ICMPVersion): either v4 or v6
            icmp_type (ICMPType | ICMPv6Type): High level category
            icmp_code (ICMPCode | ICMPv6Code): Low level category
            seq (int | None): Sequence number
            identifier (int | None): Identifier number
            checksum_valid (bool): True if checksum is valid, False otherwise
        """

        self.data = {
            "icmp_type_v4": icmp_type if version == ICMPVersion.ICMPV4 else None,
            "icmp_code_v4": icmp_code if version == ICMPVersion.ICMPV4 else None,
            "icmp_type_v6": icmp_type if version == ICMPVersion.ICMPV6 else None,
            "icmp_code_v6": icmp_code if version == ICMPVersion.ICMPV6 else None,
            "version": version,
            "seq": seq,
            "identifier": identifier,
            "checksum_valid": checksum_valid
        }
