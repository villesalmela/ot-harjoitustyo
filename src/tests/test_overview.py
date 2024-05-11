import unittest

from pandas import Timestamp, Timedelta

from main import Context
from analyzer.base_analyzer import BaseAnalyzer

class TestOverview(unittest.TestCase):

    def setUp(self) -> None:
        self.context = Context(reset_db=True)
        self.context.append("assets/dns.pcap")
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
            Timestamp('2005-03-30 11:47:46.496046'),
            Timestamp('2005-03-30 11:52:25.375359'),
            Timedelta('0 days 00:04:38.879313')
        ))
        
    def test_speed_series(self) -> None:
        bps, bps_max = self.base_analyzer.time_series_speed(interval_count_target=5)
        expected_bps = {
            Timestamp('2005-03-30 11:47:00'): 11.266666666666667,
            Timestamp('2005-03-30 11:48:00'): 3.566666666666667,
            Timestamp('2005-03-30 11:49:00'): 5.666666666666667,
            Timestamp('2005-03-30 11:50:00'): 8.266666666666667,
            Timestamp('2005-03-30 11:51:00'): 5.133333333333334,
            Timestamp('2005-03-30 11:52:00'): 27.866666666666667
        }
        expected_bps_max = {
            Timestamp('2005-03-30 11:47:00'): 298,
            Timestamp('2005-03-30 11:48:00'): 214,
            Timestamp('2005-03-30 11:49:00'): 176,
            Timestamp('2005-03-30 11:50:00'): 176,
            Timestamp('2005-03-30 11:51:00'): 150,
            Timestamp('2005-03-30 11:52:00'): 1506
        }
        self.assertEqual(bps.to_dict(), expected_bps)
        self.assertEqual(bps_max.to_dict(), expected_bps_max)