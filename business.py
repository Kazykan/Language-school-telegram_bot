from dataclasses import dataclass
from datetime import datetime


def add_time(hour: int, minute: int, day: int) -> dataclass:
    times = datetime(year=2021, month=11, day=day, hour=hour, minute=minute)
    return times
