import pandas as pd

from utils.utils import custom_round


class BaseAnalyzer:

    def __init__(self, packets: pd.DataFrame) -> None:
        self.packets = packets

    def time_series(self, interval_count_target: int) -> tuple[pd.Series, pd.Series]:
        time_df = self.packets.copy()
        time_df.set_index("packet.time", inplace=True)
        _, _, duration = self.time_range_and_duration()
        duration_seconds = int(duration.total_seconds())

        # Ensure that the interval count is between 1 and the duration in seconds
        interval_count_target = max(1, min(duration_seconds, interval_count_target))

        # Calculate the sampling frequency based on the interval count target
        sampling_freq = duration_seconds // interval_count_target

        # Ensure the sampling frequency is at least 1
        sampling_freq = max(1, sampling_freq)

        # Custom rounding
        sampling_freq = custom_round(sampling_freq)

        bytes_per_second = time_df["packet.size"].resample("s").sum().fillna(0)
        max_bytes_per_second = bytes_per_second.resample(f"{sampling_freq}s").max().fillna(0)
        bytes_per_interval = time_df["packet.size"].resample(f"{sampling_freq}s").sum().fillna(0)
        bytes_per_second = bytes_per_interval / sampling_freq
        return bytes_per_second, max_bytes_per_second

    def total_size(self) -> float:
        return self.packets["packet.size"].sum()

    def time_range_and_duration(self) -> tuple[pd.Timestamp, pd.Timestamp, pd.Timedelta]:
        time_earliest = self.packets["packet.time"].min()
        time_latest = self.packets["packet.time"].max()
        duration = time_latest - time_earliest
        return time_earliest, time_latest, duration
