import sqlite3
import json
from uuid import UUID

import pandas as pd

from layers.layers import LAYERS
from layers.properties import PROPERTIES
from storage.storage import Storage


class DBStorage(Storage):
    def __init__(self, filename: str) -> None:
        self.conn = sqlite3.connect(filename, detect_types=sqlite3.PARSE_DECLTYPES)
        self.dtype = self.build_dtypes()
        self.register_properties()
        self.register_uuid()
        self.register_json()

    def save(self, data: pd.DataFrame, name: str = "packets") -> None:
        data.to_sql(name, self.conn, if_exists="replace", dtype=self.dtype)

    def load(self, name: str = "packets") -> pd.DataFrame:
        return pd.read_sql("SELECT * FROM ?;", self.conn, index_col="packet.uid", params=(name,))

    @classmethod
    def register_uuid(cls) -> None:
        sqlite3.register_adapter(UUID, cls.adapt_uuid)
        sqlite3.register_converter('uuid', cls.convert_uuid)

    @classmethod
    def register_json(cls) -> None:
        sqlite3.register_adapter(list, cls.adapt_list)
        sqlite3.register_adapter(dict, cls.adapt_dict)
        sqlite3.register_converter('TEXT', cls.convert_text)

    @staticmethod
    def adapt_uuid(uuid_obj: UUID) -> bytes:
        return uuid_obj.bytes

    @staticmethod
    def convert_uuid(b: bytes) -> UUID:
        return UUID(bytes=b)

    @staticmethod
    def adapt_list(list_obj) -> bytes:
        return json.dumps(list_obj).encode('utf-8')

    @staticmethod
    def adapt_dict(dict_obj) -> bytes:
        return json.dumps(dict_obj).encode('utf-8')

    @staticmethod
    def convert_text(b: bytes) -> str:
        text = b.decode('utf-8')
        if (text.startswith('[') and text.endswith(']')) \
                or (text.startswith('{') and text.endswith('}')):
            return json.loads(text)
        return text

    @staticmethod
    def build_dtypes() -> dict[str, str]:
        dtype = {}
        for layer in LAYERS:
            for key, value in layer.dtypes.items():
                dtype[f"{layer.layer_type}.{layer.layer_name}.data.{key}"] = value.__name__
        dtype["packet.uid"] = "uuid"
        return dtype

    @staticmethod
    def register_properties() -> None:
        for prop in PROPERTIES:
            prop.register()
