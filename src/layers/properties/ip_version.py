from enum import Enum


class IPVersion(Enum):
    UNKNOWN = None
    IPV4 = 4
    IPV6 = 6

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN
