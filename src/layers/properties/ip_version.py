from enum import Enum


class IPVersion(Enum):
    UNKNOWN = None
    IPv4 = 4
    IPv6 = 6

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN
