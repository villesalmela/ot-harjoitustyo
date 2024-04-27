import sqlite3
from enum import Enum


class EnumProperty(Enum):
    def __conform__(self, protocol):
        if protocol is sqlite3.PrepareProtocol:
            return self.name
        return None

    @classmethod
    def register(cls):
        sqlite3.register_converter(cls.__name__, lambda b: cls[b.decode('utf-8')] if b else None)
