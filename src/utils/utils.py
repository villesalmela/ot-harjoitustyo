from numbers import Number
from enum import Enum
import json
import tldextract


def preprocess_data(data):
    """Generated with ChatGPT.

    Recursively process nested data: decode bytes to UTF-8 strings, convert numbers to integers or
    floats.
    """

    if isinstance(data, Enum):
        return data
    if isinstance(data, dict):
        # Recursively apply transformations to each key-value pair in the dictionary
        data = {preprocess_data(key): preprocess_data(value) for key, value in data.items()}
    if isinstance(data, list):
        # Apply transformations to each item in the list
        data = [preprocess_data(item) for item in data]
    if isinstance(data, bytes):
        data = data.strip(b"\x00")
        try:
            # Attempt to decode bytes to a UTF-8 string
            data = data.decode('utf-8')
        except UnicodeDecodeError:
            # Return hexadecimal representation if decoding fails
            data = data.hex()
    if isinstance(data, Number):
        try:
            # Attempt conversion to int if it matches exactly
            if data == int(data):
                data = int(data)
            else:
                data = float(data)
        except (ValueError, TypeError, OverflowError, NotImplementedError):
            # If conversion to int fails, fall back to float
            data = float(data)

    return data


def extract_2ld(fqdn):
    """Generated with ChatGPT.

    Extract the second level domain from a fully qualified domain name (FQDN).
    :param fqdn: Fully qualified domain name
    :return: 2LD and TLD combined
    """

    if not fqdn:
        raise ValueError("FQDN is empty")

    # First try with tldextract
    extracted = tldextract.extract(fqdn)
    if extracted.domain and extracted.suffix:
        # If both parts are identified, return them
        return f"{extracted.domain}.{extracted.suffix}"

    # Fallback mechanism
    parts = fqdn.split('.')

    # Basic assumption: The last two parts are the domain and TLD
    if len(parts) >= 2:
        return f"{parts[-2]}.{parts[-1]}"

    # Return the original
    return fqdn


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Enum):
            return o.name
        return super().default(o)
