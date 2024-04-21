from enum import Enum


class DNSDir(Enum):
    UNKNOWN = None
    QUERY = 0
    RESPONSE = 1

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN
