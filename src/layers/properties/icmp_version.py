from enum import Enum


class ICMPVersion(Enum):
    UNKNOWN = None
    ICMPv4 = 4
    ICMPv6 = 6

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN
