from enum import Enum


class DNSRCode(Enum):
    "Generated with ChatGPT."
    UNKNOWN = None
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

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN
