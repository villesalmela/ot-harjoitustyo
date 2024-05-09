import unittest
from config import DB_PATH


class TestDB(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_db_path(self) -> None:
        self.assertEqual(DB_PATH, "test_database.db")