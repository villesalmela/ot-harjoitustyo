from enum import IntEnum


class BOOTPOpCode(IntEnum):
    "Generated with ChatGPT."
    BOOTREQUEST = 1  # Used by a client to request configuration from servers
    BOOTREPLY = 2    # Used by a server to reply to a client's request
