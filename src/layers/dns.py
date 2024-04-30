from typing import Any

from layers.layer_config import LayerConfig
from layers.layer_level import LayerLevel
from components.enum_property import EnumProperty


class DNSDir(EnumProperty):
    """Property of DNS layer, holding Direction.
    
    Will not raise ValueError if called with invalid value, returns None instead."""
    QUERY = 0
    RESPONSE = 1


class DNSQType(EnumProperty):
    """Property of DNS layer, holding Query Type.
    
    Will not raise ValueError if called with invalid value, returns None instead.
    Generated with ChatGPT."""
    A = 1             # IPv4 address
    NS = 2            # Name server
    MD = 3            # Mail destination (Obsolete - use MX)
    MF = 4            # Mail forwarder (Obsolete - use MX)
    CNAME = 5         # Canonical name for an alias
    SOA = 6           # Start of a zone of authority
    MB = 7            # Mailbox domain name (EXPERIMENTAL)
    MG = 8            # Mail group member (EXPERIMENTAL)
    MR = 9            # Mail rename domain name (EXPERIMENTAL)
    NULL = 10         # Null RR (EXPERIMENTAL)
    WKS = 11          # Well known service description
    PTR = 12          # Domain name pointer
    HINFO = 13        # Host information
    MINFO = 14        # Mailbox or mail list information
    MX = 15           # Mail exchange
    TXT = 16          # Text strings
    RP = 17           # Responsible person
    AFSDB = 18        # AFS database location
    X25 = 19          # X.25 PSDN address
    ISDN = 20         # ISDN address
    RT = 21           # Route Through
    NSAP = 22         # NSAP address, NSAP style A record
    NSAP_PTR = 23     # NSAP pointer, domain name pointer, NSAP style
    SIG = 24          # Security signature
    KEY = 25          # Security key
    PX = 26           # X.400 mail mapping information
    GPOS = 27         # Geographical Position
    AAAA = 28         # IPv6 address
    LOC = 29          # Location Information
    NXT = 30          # Next Domain (Obsolete)
    EID = 31          # Endpoint Identifier (Obsolete)
    NIMLOC = 32       # Nimrod Locator (Obsolete)
    SRV = 33          # Server Selection
    ATMA = 34         # ATM Address (Obsolete)
    NAPTR = 35        # Naming Authority Pointer
    KX = 36           # Key Exchanger
    CERT = 37         # Certificate
    A6 = 38           # IPv6 Address (Obsolete - use AAAA)
    DNAME = 39        # Non-Terminal DNS Name Redirection
    SINK = 40         # Kitchen sink (Experimental)
    OPT = 41          # Option
    APL = 42          # Address Prefix List
    DS = 43           # Delegation Signer
    SSHFP = 44        # SSH Key Fingerprint
    IPSECKEY = 45     # IPSEC Key
    RRSIG = 46        # DNSSEC Signature
    NSEC = 47         # Next Secure Record
    DNSKEY = 48       # DNS Key
    DHCID = 49        # DHCP Identifier
    NSEC3 = 50        # NSEC record version 3
    NSEC3PARAM = 51   # NSEC3 parameters
    TLSA = 52         # TLSA certificate association
    SMIMEA = 53       # S/MIME certificate association
    HIP = 55          # Host Identity Protocol
    NINFO = 56        # NINFO
    RKEY = 57         # RKEY
    TALINK = 58       # Trust Anchor LINK
    CDS = 59          # Child DS
    CDNSKEY = 60      # DNSKEY(s) the Child wants reflected in DS
    OPENPGPKEY = 61   # OpenPGP Key
    CSYNC = 62        # Child-To-Parent Synchronization
    ZONEMD = 63       # Message Digest for DNS Zone
    SVCB = 64         # Service Binding
    HTTPS = 65        # HTTPS Binding
    TKEY = 249        # Transaction Key
    TSIG = 250        # Transaction Signature
    IXFR = 251        # Incremental zone transfer
    AXFR = 252        # Transfer of an entire zone
    ANY = 255         # Wildcard match
    URI = 256         # URI
    CAA = 257         # Certification Authority Authorization

class DNSOpCode(EnumProperty):
    """Property of DNS layer, holding Direction.
    
    Will not raise ValueError if called with invalid value, returns None instead.
    Generated with ChatGPT."""
    QUERY = 0         # Standard query (RFC 1035)
    IQUERY = 1        # Inverse query (deprecated by RFC 3425)
    STATUS = 2        # Server status request (RFC 1035)
    # 3 is unassigned
    NOTIFY = 4        # Notify (RFC 1996)
    UPDATE = 5        # Update (RFC 2136)
    STATEFUL = 6      # DNS Stateful Operations (DSO) (RFC 8490)
    # Opcodes 7-15 are reserved for future use

class DNSRCode(EnumProperty):
    """Property of DNS layer, holding Return Code.
    
    Will not raise ValueError if called with invalid value, returns None instead.
    Generated with ChatGPT."""
    NOERROR = 0   # No Error
    FORMERR = 1   # Format Error
    SERVFAIL = 2  # Server Failure
    NXDOMAIN = 3  # Non-Existent Domain
    NOTIMP = 4    # Not Implemented
    REFUSED = 5   # Query Refused
    YXDOMAIN = 6  # Name Exists when it should not
    YXRRSET = 7   # RR Set Exists when it should not
    NXRRSET = 8   # RR Set that should exist does not
    NOTAUTH = 9   # Server Not Authoritative for zone
    NOTZONE = 10  # Name not contained in zone

class DNS(LayerConfig):
    """Configuration for DNS layer."""

    layer_type = LayerLevel.APPLICATION
    layer_name = "DNS"
    data: dict[str, Any]

    def __init__(self,
                 transaction_id: int,
                 direction: DNSDir,
                 opcode: DNSOpCode,
                 qtype: DNSQType,
                 rcode: DNSRCode,
                 qname: str | None,
                 answers: list[dict[str, str | int]] | None = None
                 ) -> None:
        """Initializes DNS configuration object with provided details.

        Args:
            transaction_id (int): id number that identifies transactions
            direction (DNSDir): indicating either query or response
            opcode (DNSOpCode): Operation Code
            qtype (DNSQType): Query Type
            rcode (DNSRCode): Return Code
            qname (str | None): the queried name
            answers (list[dict[str, str  |  int]] | None, optional): various answer details. Defaults to None.
        """

        self.data = {
            "transaction_id": transaction_id,
            "direction": direction,
            "opcode": opcode,
            "qtype": qtype,
            "rcode": rcode,
            "qname": qname,
            "answers": answers
        }
