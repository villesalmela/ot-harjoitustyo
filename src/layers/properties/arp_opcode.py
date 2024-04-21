from enum import Enum


class ARPOpCode(Enum):
    "Generated with ChatGPT."
    UNKNOWN = None
    REQUEST = 1       # ARP Request
    REPLY = 2         # ARP Reply
    RARP_REQUEST = 3  # Reverse ARP Request
    RARP_REPLY = 4    # Reverse ARP Reply
    DRARP_REQUEST = 5  # Dynamic RARP Request
    DRARP_REPLY = 6   # Dynamic RARP Reply
    DRARP_ERROR = 7   # Dynamic RARP Error
    INARP_REQUEST = 8  # InARP Request
    INARP_REPLY = 9   # InARP Reply

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN
