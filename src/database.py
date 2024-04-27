import sqlite3
import json
from uuid import UUID

import pandas as pd
import numpy as np

from layers.dns import DNS, DNSDir, DNSOpCode, DNSQType, DNSRCode
from layers.dhcp import DHCP, DHCPMessageType, BOOTPOpCode
from layers.arp import ARP, ARPOpCode, HardwareType
from layers.icmp import ICMP, ICMPCode, ICMPType, ICMPv6Code, ICMPv6Type, ICMPVersion
from layers.ip import IP, IPVersion
from layers.sll import SLL, CookedPacketType
from layers.ethernet import Ethernet

ENUM_PROPERTIES = [
    DNSDir, DNSOpCode, DNSQType, DNSRCode,
    DHCPMessageType, BOOTPOpCode,
    ARPOpCode, HardwareType,
    ICMPCode, ICMPType, ICMPv6Code, ICMPv6Type, ICMPVersion,
    IPVersion,
    CookedPacketType
]

BOOLEAN_COLUMNS = [
    "NETWORK.IP.data.checksum_valid",
    "TRANSPORT.TCP.data.checksum_valid",
    "TRANSPORT.UDP.data.checksum_valid",
    "TRANSPORT.ICMP.data.checksum_valid"
]

# Handle conversion of UUID objects


def adapt_uuid(uuid_obj: UUID) -> bytes:
    return uuid_obj.bytes


def convert_uuid(b: bytes) -> UUID:
    return UUID(bytes=b)


sqlite3.register_adapter(UUID, adapt_uuid)
sqlite3.register_converter('uuid', convert_uuid)

# Handle conversion of json-like objects


def adapt_list(list_obj) -> bytes:
    return json.dumps(list_obj).encode('utf-8')


def adapt_dict(dict_obj) -> bytes:
    return json.dumps(dict_obj).encode('utf-8')


def convert_text(b: bytes) -> str:
    text = b.decode('utf-8')
    if (text.startswith('[') and text.endswith(']')) \
            or (text.startswith('{') and text.endswith('}')):
        return json.loads(text)
    return text


sqlite3.register_adapter(list, adapt_list)
sqlite3.register_adapter(dict, adapt_dict)
sqlite3.register_converter('TEXT', convert_text)

# Handle conversion of EnumProperty objects
for enum in ENUM_PROPERTIES:
    enum.register()

# Handle conversion of boolean objects


def fix_bool(df: pd.DataFrame) -> None:
    for col in BOOLEAN_COLUMNS:
        if col in df:
            df[col] = df[col].astype("boolean")


# Get types for database schema
def build_dtypes() -> dict[str, str]:
    dtype = {}
    for layer in [ARP, DHCP, DNS, ICMP, IP, SLL, Ethernet]:
        dtype.update(layer.get_db_types())
    dtype["packet.uid"] = "uuid"
    return dtype

# Adjust dataframe dtypes before saving to context


def adjust_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    fix_bool(df)
    return df.replace({"": pd.NA, None: pd.NA, np.nan: pd.NA}).convert_dtypes()
