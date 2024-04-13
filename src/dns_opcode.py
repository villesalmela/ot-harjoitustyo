"Generated with ChatGPT"

from enum import IntEnum


class DNSOpCode(IntEnum):
    QUERY = 0         # Standard query (RFC 1035)
    IQUERY = 1        # Inverse query (deprecated by RFC 3425)
    STATUS = 2        # Server status request (RFC 1035)
    # 3 is unassigned
    NOTIFY = 4        # Notify (RFC 1996)
    UPDATE = 5        # Update (RFC 2136)
    STATEFUL = 6      # DNS Stateful Operations (DSO) (RFC 8490)
    # Opcodes 7-15 are reserved for future use
