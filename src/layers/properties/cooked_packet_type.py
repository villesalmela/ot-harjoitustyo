from enum import Enum


class CookedPacketType(Enum):
    UNKNOWN = None
    UNICAST = 0
    BROADCAST = 1
    MULTICAST = 2
    UNICAST_TO_ANOTHER_HOST = 3
    SENT_BY_US = 4
