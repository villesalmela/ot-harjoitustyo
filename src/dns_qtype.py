"Generated with ChatGPT"

from enum import IntEnum

class DNSQType(IntEnum):
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
    ANY = 255         # Wildcard match


