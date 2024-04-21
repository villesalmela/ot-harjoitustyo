from enum import Enum


class BOOTPOpCode(Enum):
    "Generated with ChatGPT."
    UNKNOWN = None
    BOOTREQUEST = 1  # Used by a client to request configuration from servers
    BOOTREPLY = 2    # Used by a server to reply to a client's request

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN
