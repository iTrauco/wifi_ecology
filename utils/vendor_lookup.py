# vendor_lookup.py - Utility for MAC vendor lookups

OUI_VENDOR_MAP = {
    "00:1A:2B": "Apple Inc.",
    "00:1B:44": "Dell Inc.",
    "B8:27:EB": "Raspberry Pi Foundation",
    "3C:5A:B4": "Google Inc.",
    "F4:5C:89": "Amazon Technologies Inc.",
    # Add more as needed or import from a real DB later
}

def get_vendor(mac_address: str) -> str:
    prefix = mac_address.upper().replace("-", ":")[0:8]
    oui = ":".join(prefix.split(":")[:3])
    return OUI_VENDOR_MAP.get(oui, "Unknown Vendor")
