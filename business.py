from dataclasses import dataclass
from datetime import datetime, date


def add_time(hour: int, minute: int, day: int) -> dataclass:
    times = datetime(year=2021, month=11, day=day, hour=hour, minute=minute)
    return times


def add_date(dates: str) -> date:
    temp = dates.split('.')
    edit_date = date(year=int(temp[2]), month=int(temp[1]), day=int(temp[0]))
    return edit_date


print(add_date('23.11.1956'))