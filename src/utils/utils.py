from numbers import Number
from enum import Enum
import json
import tldextract


def preprocess_data(data):
    """Generated with ChatGPT.

    Recursively process nested data: decode bytes to UTF-8 strings, convert numbers to integers or
    floats.
    """

    allowed_types = (dict, list, str, Enum, int, float, type(None))

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
    if not isinstance(data, allowed_types):
        # If the data type is not in the allowed types, convert it to a string
        print(f"Encountered unexpected data type: {type(data)}, {data=}")
        data = str(data)

    return data


def extract_2ld(fqdn):
    """Generated with ChatGPT.

    Extract the second level domain from a fully qualified domain name (FQDN).
    :param fqdn: Fully qualified domain name
    :return: 2LD and TLD combined
    """

    if not fqdn:
        return ""

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


def flatten_dict(d, parent_key='', sep='.'):
    """Generated with ChatGPT."""
    items = []

    def process_item(key, value, prefix=''):
        # Construct the full key from prefix and current key with proper handling for nested lists
        if isinstance(key, int):  # This is a list index, handle it without a separator
            full_key = f"{prefix}[{key}]"
        else:
            full_key = f"{prefix}{sep}{key}" if prefix else key

        if isinstance(value, dict):
            # Recurse into dictionaries
            for sub_key, sub_val in flatten_dict(value, full_key, sep).items():
                items.append((sub_key, sub_val))
        elif isinstance(value, list):
            # Handle list, may contain dicts or other lists
            list_items = {}
            simple_values = []
            dict_keys = set()
            # First collect all unique keys from each dictionary in the list
            for item in value:
                if isinstance(item, dict):
                    dict_keys.update(item.keys())

            for i, item in enumerate(value):
                if isinstance(item, dict):
                    for key in dict_keys:
                        list_items.setdefault(
                            f"{full_key}{sep}{key}", []).append(
                            item.get(
                                key, None))
                elif isinstance(item, list):
                    # Recursive call to handle nested lists with correct indexing
                    process_item(i, item, full_key)
                else:
                    simple_values.append(item)

            for list_key, list_vals in list_items.items():
                items.append((list_key, list_vals))
            if simple_values:
                items.append((full_key, simple_values))
        else:
            items.append((full_key, value))

    for key, val in d.items():
        process_item(key, val, parent_key)

    return dict(items)
