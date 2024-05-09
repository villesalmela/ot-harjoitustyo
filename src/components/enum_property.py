import sqlite3
from enum import Enum, EnumMeta


class EnumPropertyMeta(EnumMeta):
    def __call__(cls, *args, **kwds):
        """Prevents instantiation of the base class EnumProperty."""
        if cls.__name__ == "EnumProperty":
            raise ValueError(f"Cannot instantiate {cls.__name__}, it's a base class.")
        return super().__call__(*args, **kwds)


class EnumProperty(Enum, metaclass=EnumPropertyMeta):
    """Parent for all layer properties, provides the common functions shared by all of them."""

    def __init_subclass__(cls) -> None:
        """Ensures that all sub-classes of EnumProperty have an UNKNOWN value defined
        and it's not overridden."""
        if hasattr(cls, "UNKNOWN"):
            raise ValueError("EnumProperty sub-classes cannot have an UNKNOWN value defined.")
        cls.UNKNOWN = None
        return super().__init_subclass__()

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
