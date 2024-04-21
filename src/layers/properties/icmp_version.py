from enum import Enum


class ICMPVersion(Enum):
    UNKNOWN = None
    ICMPV4 = 4
    ICMPV6 = 6

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN
