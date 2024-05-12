from threading import Timer
from typing import Callable
from numbers import Number
from enum import Enum
import json
from collections import defaultdict
from pathlib import Path

import tldextract
import pandas as pd
import humanize
from config import FILESIZE_LIMIT_BYTES


def preprocess_bytes(data: bytes) -> str:
    """Strip null bytes and decode to UTF-8 string, or return hex representation if decoding fails.

    Args:
        data (bytes): Data to preprocess

    Returns:
        str: Processed data
    """
    data = data.strip(b"\x00")
    try:
        str_data = data.decode('utf-8')
    except UnicodeDecodeError:
        str_data = data.hex()
    return str_data


def preprocess_numbers(data) -> int | float:
    """Convert data to int or float, depending on the type.

    Args:
        data: Data to preprocess

    Returns:
        int | float: Processed data
    """
    try:
        # Attempt conversion to int if it matches exactly
        data = int(data) if data == int(data) else float(data)
    except (ValueError, TypeError, OverflowError, NotImplementedError):
        data = float(data)
    return data


def preprocess_data(data):
    """Generated with ChatGPT.

    Recursively process nested data: decode bytes to UTF-8 strings, convert numbers to integers or
    floats.
    """

    if isinstance(data, (Enum, bool, type(None))):
        return data
    if isinstance(data, dict):
        # Recursively apply transformations to each key-value pair in the dictionary
        data = {preprocess_data(key): preprocess_data(value) for key, value in data.items()}
    elif isinstance(data, list):
        # Apply transformations to each item in the list
        data = [preprocess_data(item) for item in data]
    elif isinstance(data, bytes):
        data = preprocess_bytes(data)
    elif isinstance(data, Number):
        data = preprocess_numbers(data)
    if not isinstance(data, (dict, list, str, int, float)):
        try:
            # If the data type is not in the allowed types, convert it to a string
            data = str(data)
        except Exception as e:
            raise ValueError(f"Unsupported data type: {type(data)}: {repr(data)}") from e

    return data


def extract_2ld(fqdn: str):
    """Generated with ChatGPT.

    Extract the second level domain from a fully qualified domain name (FQDN).

    Args:
        fqdn (str): Fully qualified domain name

    Returns:
        str: Second level domain or pd.NA if the input is missing
    """

    if pd.isna(fqdn):
        return pd.NA

    extracted = tldextract.extract(fqdn)
    if extracted.domain and extracted.suffix:
        return f"{extracted.domain}.{extracted.suffix}"

    # Fallback mechanism
    parts = fqdn.split('.')
    if len(parts) >= 2:
        return f"{parts[-2]}.{parts[-1]}"
    return fqdn


class JSONEncoder(json.JSONEncoder):
    """Custom JSON encoder that converts Enum values to their names and tuple keys to strings.
    """
    def default(self, o):
        if isinstance(o, Enum):
            return o.name
        return super().default(o)

    def tuple_to_string(self, value):
        if isinstance(value, tuple):
            return f"({", ".join(str(k) for k in value)})"
        return value

    def encode(self, o):
        if isinstance(o, dict):
            # Convert tuple keys to strings
            return super().encode({self.tuple_to_string(k): v for k, v in o.items()})
        return super().encode(o)


def _collect_keys(data: list):
    dict_keys = set()
    for item in data:
        if isinstance(item, dict):
            dict_keys.update(item.keys())
    return dict_keys


def _append_value_if_any(source_dict, dict_keys, target_dict, prefix, sep):
    for dkey in dict_keys:
        target_dict[f"{prefix}{sep}{dkey}"].append(source_dict.get(dkey, None))


def _process_item(items, sep, key, value, prefix=''):
    full_key = f"{prefix}{sep}{key}" if prefix else key

    if isinstance(value, dict):
        for sub_key, sub_val in flatten_dict(value, full_key, sep).items():
            items.append((sub_key, sub_val))
    elif isinstance(value, list):
        list_items = defaultdict(list)
        simple_values = []
        dict_keys = _collect_keys(value)

        for i, item in enumerate(value):
            if isinstance(item, dict):
                _append_value_if_any(item, dict_keys, list_items, full_key, sep)
            elif isinstance(item, list):
                _process_item(items, sep, i, item, full_key)
            else:
                simple_values.append(item)

        for list_key, list_vals in list_items.items():
            items.append((list_key, list_vals))
        if simple_values:
            items.append((full_key, simple_values))
    else:
        items.append((full_key, value))


def flatten_dict(d: dict, parent_key="", sep=".") -> dict:
    """Flatten a nested dictionary.

    Generated with ChatGPT.

    Nested dictionaries are flattened into a single level dictionary with dot-separated keys
    representing the hierarchy of the original keys.
    
    Lists are flattened into separate keys with the list index as the key.

    Args:
        d (dict): Dictionary to flatten
        parent_key (str, optional): key prefix for nested dictionaries. Defaults to "".
        sep (str, optional): separator for nested keys. Defaults to ".".

    Returns:
        dict: Flattened dictionary
    """
    items = []
    for key, val in d.items():
        _process_item(items, sep, key, val, parent_key)
    return dict(items)


def convert_mac(mac: bytes) -> str:
    """Convert MAC address from bytes to a human-readable string.

    Generated with ChatGPT.

    Args:
        mac (bytes): MAC address in bytes

    Returns:
        str: MAC address in human-readable format
    """
    return ":".join([f"{int(byte):02x}" for byte in mac.strip(b"\x00")])


def scale_bits(bits: pd.Series | Number) -> tuple[pd.Series | Number, str]:
    """Scale bits to Kbits or Mbits if necessary.

    Args:
        bits (pd.Series | Number): Bits to scale

    Returns:
        tuple[pd.Series | Number, str]: Scaled bits, unit
    """
    if isinstance(bits, pd.Series):
        orig_scale = bits.max()
    else:
        orig_scale = bits
    if orig_scale < 1e3:
        unit = 'bits'
        scaled_bits = bits
    elif orig_scale < 1e6:
        unit = 'Kbits'
        scaled_bits = bits / 1e3
    else:
        unit = 'Mbits'
        scaled_bits = bits / 1e6
    return scaled_bits, unit


def convert_to_bits(bytes_value):
    """Multiply the value(s) by 8 to convert bytes to bits."""
    return bytes_value * 8


def custom_round(x: int | float) -> int:
    """Round a number to the nearest 1, 2, 5, or multiple of 10.

    Args:
        x (int | float): Number to round

    Raises:
        ValueError: If the input is negative

    Returns:
        int: Rounded number
    """
    if x < 0:
        raise ValueError
    if x < 1.5:
        return 1
    if x < 2.5:
        return 2
    if x < 7.5:
        return 5
    if x < 10:
        return 10

    scale = len(str(x).split('.', maxsplit=1)[0]) - 1
    return round(x / (10 ** scale)) * (10 ** scale)


def check_file(filename: str):
    """Check if the file exists, is a PCAP file, and is within the size limit.

    Args:
        filename (str): Path to the file

    Raises:
        FileNotFoundError: if file is not found, not a PCAP file, or exceeds the size limit
    """
    file = Path(filename)
    size = file.stat().st_size
    suffix = file.suffix

    if not (file.exists() and file.is_file()):
        raise FileNotFoundError(f"File not found: {filename}")

    if suffix not in (".pcap", ".pcapng"):
        raise FileNotFoundError(f"File must be a PCAP file, not '{suffix}'")

    if size > FILESIZE_LIMIT_BYTES:
        raise FileNotFoundError(
            f"File size exceeds the limit of {humanize.naturalsize(FILESIZE_LIMIT_BYTES)}")


def start_timer(seconds: int, command: Callable) -> Timer:
    """Start a timer that executes a command after a specified number of seconds.

    Args:
        seconds (int): Number of seconds to wait
        command (Callable): Function to execute

    Returns:
        Timer: Timer object
    """
    timer = Timer(seconds, command)
    timer.start()
    return timer
