from enum import StrEnum


class LayerLevel(StrEnum):
    """Enumeration of layer levels in the network stack."""
    LINK = "LINK"
    NETWORK = "NETWORK"
    TRANSPORT = "TRANSPORT"
    APPLICATION = "APPLICATION"
