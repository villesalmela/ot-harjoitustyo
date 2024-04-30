import sqlite3
from enum import EnumMeta, Enum

class ExtendableEnumMeta(EnumMeta):
    """Customized EnumMeta class that allows for the definition of members on the parent level."""
    
    @classmethod
    def _check_for_existing_members_(mcls, class_name, bases):
        """By overriding this function in the Enum metaclass, we can now define members on the
        parent level without error.
        """
        pass


class EnumProperty(Enum, metaclass=ExtendableEnumMeta):
    """Parent for all layer properties, provides the common functions shared by all of them.

    Args:
        Enum (class): Inherits the Enum class.
    """
    
    UNKNOWN = None

    @classmethod
    def _missing_(cls, value):
        """When an invalid value is passed to the class, return the UNKNOWN value."""
        return cls.UNKNOWN

    def __conform__(self, protocol):
        """When writing this custom object to a table, adapt this custom object to a type that
        SQLite natively understands.

        Args:
            protocol: SQLite passes a PrepareProtocol object here.

        Returns:
            str: Name of the property if called by SQLite, None otherwise.
        """
        if protocol is sqlite3.PrepareProtocol:
            return self.name
        return None

    @classmethod
    def register(cls):
        """Registers a converter with SQLite, that will be used to convert the object from bytes (as
        stored in the table) back to its original type."""
        sqlite3.register_converter(cls.__name__, lambda b: cls[b.decode('utf-8')] if b else None)
