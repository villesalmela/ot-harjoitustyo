import sqlite3
import json
from uuid import UUID

import pandas as pd

from layers.dns import DNS, DNSDir, DNSOpCode, DNSQType, DNSRCode
from layers.dhcp import DHCP, DHCPMessageType, BOOTPOpCode
from layers.arp import ARP, ARPOpCode, HardwareType
from layers.icmp import ICMP, ICMPCode, ICMPType, ICMPv6Code, ICMPv6Type, ICMPVersion
from layers.ip import IP, IPVersion
from layers.sll import SLL, CookedPacketType
from layers.ethernet import Ethernet
from components.storage import Storage

ENUM_PROPERTIES = [
    DNSDir, DNSOpCode, DNSQType, DNSRCode,
    DHCPMessageType, BOOTPOpCode,
    ARPOpCode, HardwareType,
    ICMPCode, ICMPType, ICMPv6Code, ICMPv6Type, ICMPVersion,
    IPVersion,
    CookedPacketType
]


class DBStorage(Storage):
    def __init__(self, filename: str) -> None:
        self.conn = sqlite3.connect(filename, detect_types=sqlite3.PARSE_DECLTYPES)
        self.dtype = self.build_dtypes()
        sqlite3.register_adapter(UUID, self.adapt_uuid)
        sqlite3.register_converter('uuid', self.convert_uuid)
        sqlite3.register_adapter(list, self.adapt_list)
        sqlite3.register_adapter(dict, self.adapt_dict)
        sqlite3.register_converter('TEXT', self.convert_text)

        # Handle conversion of EnumProperty objects
        for enum in ENUM_PROPERTIES:
            enum.register()

    def save(self, data: pd.DataFrame, name: str = "packets") -> None:
        data.to_sql(name, self.conn, if_exists="replace", dtype=self.dtype)

    def load(self, name: str = "packets") -> pd.DataFrame:
        return pd.read_sql(f"SELECT * FROM {name}", self.conn, index_col="packet.uid")

    # Handle conversion of UUID objects
    @staticmethod
    def adapt_uuid(uuid_obj: UUID) -> bytes:
        return uuid_obj.bytes

    @staticmethod
    def convert_uuid(b: bytes) -> UUID:
        return UUID(bytes=b)

    # Handle conversion of json-like objects
    @staticmethod
    def adapt_list(list_obj) -> bytes:
        return json.dumps(list_obj).encode('utf-8')

    @staticmethod
    def adapt_dict(dict_obj) -> bytes:
        return json.dumps(dict_obj).encode('utf-8')

    @staticmethod
    def convert_text(b: bytes) -> str:
        text = b.decode('utf-8')
        if (text.startswith('[') and text.endswith(']')) \
                or (text.startswith('{') and text.endswith('}')):
            return json.loads(text)
        return text

    # Get types for database schema
    @staticmethod
    def build_dtypes() -> dict[str, str]:
        dtype = {}
        for layer in [ARP, DHCP, DNS, ICMP, IP, SLL, Ethernet]:
            dtype.update(layer.get_db_types())
        dtype["packet.uid"] = "uuid"
        return dtype
