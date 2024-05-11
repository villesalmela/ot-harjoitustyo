import unittest
import pandas as pd
import uuid

from config import DB_PATH
from storage.database import DBStorage
from main import Context

DB_PATH_TEST = "test_database.db"


class TestDB(unittest.TestCase):

    def setUp(self) -> None:
        self.context = Context(reset_db=True)
        self.context.append("assets/dns.pcap")
        self.storage = self.context.storage
        self.df = self.context.get_df()

    def tearDown(self) -> None:
        self.storage.conn.close()

    def test_db_path(self) -> None:
        self.assertEqual(DB_PATH, DB_PATH_TEST)

    def test_save(self) -> None:
        self.assertFalse(self.storage.slot_exists("test1"))
        self.storage.save(self.df, "test1")
        self.assertTrue(self.storage.slot_exists("test1"))

    def test_load(self) -> None:
        self.storage.save(self.df, "test2")
        df = self.storage.load("test2")
        self.assertTrue(df.equals(self.df))

    def test_del(self) -> None:
        self.storage.save(self.df, "test3")
        self.assertTrue(self.storage.slot_exists("test3"))
        self.storage.del_slot("test3")
        self.assertFalse(self.storage.slot_exists("test3"))

    def test_list(self) -> None:
        self.storage.save(self.df, "test4")
        self.storage.save(self.df, "test5")
        self.assertEqual(self.storage.list_slots(), ["test4", "test5"])
