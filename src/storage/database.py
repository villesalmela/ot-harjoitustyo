import sqlite3
import json
from uuid import UUID
from pathlib import Path

import pandas as pd
import numpy as np

from layers.layers import LAYERS
from layers.properties import PROPERTIES
from storage.storage import Storage


BOOLEAN_COLUMNS = [
    "NETWORK.IP.data.checksum_valid",
    "TRANSPORT.TCP.data.checksum_valid",
    "TRANSPORT.UDP.data.checksum_valid",
    "TRANSPORT.ICMP.data.checksum_valid"
]


class DBStorage(Storage):
    """SQLite database storage backend."""

    def __init__(self, filename: str, reset=False) -> None:
        self.filename = filename
        if reset:
            self.reset()
        self.conn = sqlite3.connect(filename, detect_types=sqlite3.PARSE_DECLTYPES)
        self.dtype = self._build_dtypes()
        self._register_properties()
        self._register_uuid()
        self._register_json()
        self._create_slot_table()

    def reset(self) -> None:
        """Delete the database file if it exists.
        """
        file = Path(self.filename)
        if file.exists():
            file.unlink()

    @staticmethod
    def adjust_dtypes(df: pd.DataFrame) -> pd.DataFrame:
        """Adjusts the data types of the DataFrame.

        Because of the way the data is stored in the database, some columns need to be converted
        to the correct data type.

        Args:
            df (pd.DataFrame): DataFrame to adjust

        Returns:
            pd.DataFrame: Adjusted DataFrame
        """
        for col in BOOLEAN_COLUMNS:
            if col in df:
                df[col] = df[col].astype("boolean")
        return df.replace({"": pd.NA, None: pd.NA, np.nan: pd.NA}).convert_dtypes()

    def _create_slot_table(self) -> None:
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS slots (id INTEGER PRIMARY KEY,\
                        name TEXT UNIQUE);")
        self.conn.commit()

    def _get_slot_id(self, name: str) -> str:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM slots WHERE name = ?;", [name])
        result = cursor.fetchone()
        if result:
            slot_id = result[0]
        else:
            cursor.execute("INSERT INTO slots (name) VALUES (?);", [name])
            slot_id = cursor.lastrowid
            self.conn.commit()
        return f"t_{slot_id}"

    def slot_exists(self, name: str) -> bool:
        """Check if a save slot exists.

        Args:
            name (str): name of the save slot

        Returns:
            bool: True if the slot exists
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM slots WHERE name = ?;", [name])
        return cursor.fetchone() is not None

    def save(self, data: pd.DataFrame, name: str, new: bool = False) -> None:
        """Save the DataFrame to the database.

        Args:
            data (pd.DataFrame): DataFrame to save
            name (str): name of the save slot
            new (bool, optional): If True, the slot will not be overwritten if it already exists.
                Defaults to False.

        Raises:
            ValueError: If new is True amd the slot already exists
        """
        if new and self.slot_exists(name):
            raise ValueError(f"Slot {name} already exists.")
        slot = self._get_slot_id(name)
        data.to_sql(slot, self.conn, if_exists="replace", dtype=self.dtype)

    def load(self, name: str) -> pd.DataFrame:
        """Load the DataFrame from the database.

        Args:
            name (str): name of the save slot

        Returns:
            pd.DataFrame: loaded DataFrame
        """
        slot = self._get_slot_id(name)
        df = pd.read_sql(f"SELECT * FROM {slot};", self.conn, index_col="packet.uid")
        return self.adjust_dtypes(df)

    def list_slots(self) -> list[str]:
        """List all available save slots.

        Returns:
            list[str]: list of slot names
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM slots;")
        return [row[0] for row in cursor.fetchall()]

    def del_slot(self, name: str) -> None:
        """Delete a save slot.

        Args:
            name (str): name of the save slot
        """
        slot = self._get_slot_id(name)
        cursor = self.conn.cursor()
        cursor.execute(f"DROP TABLE {slot};")
        cursor.execute("DELETE FROM slots WHERE name = ?;", [name])
        self.conn.commit()

    @classmethod
    def _register_uuid(cls) -> None:
        sqlite3.register_adapter(UUID, cls._adapt_uuid)
        sqlite3.register_converter('uuid', cls._convert_uuid)

    @classmethod
    def _register_json(cls) -> None:
        sqlite3.register_adapter(list, cls._adapt_list)
        sqlite3.register_adapter(dict, cls._adapt_dict)
        sqlite3.register_converter('TEXT', cls._convert_text)

    @staticmethod
    def _adapt_uuid(uuid_obj: UUID) -> bytes:
        return uuid_obj.bytes

    @staticmethod
    def _convert_uuid(b: bytes) -> UUID:
        return UUID(bytes=b)

    @staticmethod
    def _adapt_list(list_obj) -> bytes:
        return json.dumps(list_obj).encode('utf-8')

    @staticmethod
    def _adapt_dict(dict_obj) -> bytes:
        return json.dumps(dict_obj).encode('utf-8')

    @staticmethod
    def _convert_text(b: bytes) -> str:
        text = b.decode('utf-8')
        if (text.startswith('[') and text.endswith(']')) \
                or (text.startswith('{') and text.endswith('}')):
            return json.loads(text)
        return text

    @staticmethod
    def _build_dtypes() -> dict[str, str]:
        dtype = {}
        for layer in LAYERS:
            for key, value in layer.dtypes.items():
                dtype[f"{layer.layer_type}.{layer.layer_name}.data.{key}"] = value.__name__
        dtype["packet.uid"] = "uuid"
        return dtype

    @staticmethod
    def _register_properties() -> None:
        for prop in PROPERTIES:
            prop.register()
