from typing import Any

from layers.layer_config import LayerConfig
from layers.layer_level import LayerLevel
from components.enum_property import EnumProperty


class ARPOpCode(EnumProperty):
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


class HardwareType(EnumProperty):
    "Generated with ChatGPT."
    UNKNOWN = None
    ETHERNET_10MB = 1
    ETHERNET_3MB = 2
    AX_25 = 3
    PROTEON = 4
    CHAOS = 5
    IEEE802 = 6
    ARCNET = 7
    HYPERCHANNEL = 8
    LANSTAR = 9
    AUTONET = 10
    LOCALTALK = 11
    LOCALNET = 12
    ULTRA_LINK = 13
    SMDS = 14
    FRAME_RELAY = 15
    ATM_JXB2 = 16
    HDLC = 17
    FIBRE_CHANNEL = 18
    ATM_RFC2225 = 19
    SERIAL_LINE = 20
    ATM_BURROWS = 21
    MIL_STD_188_220 = 22
    METRICOM = 23
    IEEE_1394 = 24
    MAPOS = 25
    TWINAXIAL = 26
    EUI_64 = 27
    HIPARP = 28
    IP_ISO_7816_3 = 29
    ARPSEC = 30
    IPSEC_TUNNEL = 31
    INFINIBAND = 32
    TIA_102 = 33
    WIEGAND = 34
    PURE_IP = 35
    HW_EXP1 = 36
    HFI = 37
    UNIFIED_BUS = 38
    HW_EXP2 = 256
    AETHERNET = 257


class ARP(LayerConfig):

    layer_type = LayerLevel.NETWORK
    layer_name = "ARP"
    data: dict[str, Any]

    def __init__(
            self,
            hwtype: HardwareType,
            opcode: ARPOpCode,
            hwsrc: str,
            hwdst: str,
            psrc: str,
            pdst: str) -> None:

        self.data = {
            "hwtype": hwtype,
            "opcode": opcode,
            "hwsrc": hwsrc,
            "hwdst": hwdst,
            "psrc": psrc,
            "pdst": pdst
        }
