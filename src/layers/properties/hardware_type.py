from enum import Enum


class HardwareType(Enum):
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
