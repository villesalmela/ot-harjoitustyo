import unittest

from pandas import Timestamp, Timedelta

from main import Context
from analyzer.base_analyzer import BaseAnalyzer


ASSET_PATH = "assets/dns.pcapng"


class TestOverview(unittest.TestCase):

    def setUp(self) -> None:
        self.context = Context(reset_db=True)
        self.context.append(ASSET_PATH)
        self.storage = self.context.storage
        self.df = self.context.get_df()
        self.base_analyzer = BaseAnalyzer(self.df)

    def tearDown(self) -> None:
        self.storage.conn.close()

    def test_size(self) -> None:
        self.assertEqual(self.base_analyzer.total_size(), 3706)

    def test_packet_count(self) -> None:
        self.assertEqual(self.base_analyzer.packet_count(), 38)

    def test_time_stats(self) -> None:
        self.assertEqual(self.base_analyzer.time_range_and_duration(), (
            Timestamp('2023-02-06 20:16:07'),
            Timestamp('2023-02-06 20:16:59.999999'),
            Timedelta('0 days 00:00:52.999999')
        ))

    def test_speed_series(self) -> None:
        bps, bps_max = self.base_analyzer.time_series_speed(interval_count_target=5)
        expected_bps = {
            Timestamp('2023-02-06 20:16:00'): 67.6,
            Timestamp('2023-02-06 20:16:10'): 21.4,
            Timestamp('2023-02-06 20:16:20'): 34.0,
            Timestamp('2023-02-06 20:16:30'): 17.6,
            Timestamp('2023-02-06 20:16:40'): 32.0,
            Timestamp('2023-02-06 20:16:50'): 198.0
        }
        expected_bps_max = {
            Timestamp('2023-02-06 20:16:00'): 536,
            Timestamp('2023-02-06 20:16:10'): 214,
            Timestamp('2023-02-06 20:16:20'): 176,
            Timestamp('2023-02-06 20:16:30'): 176,
            Timestamp('2023-02-06 20:16:40'): 168,
            Timestamp('2023-02-06 20:16:50'): 1506
        }
        self.assertEqual(bps.to_dict(), expected_bps)
        self.assertEqual(bps_max.to_dict(), expected_bps_max)
