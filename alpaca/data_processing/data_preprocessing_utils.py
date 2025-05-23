from alpaca.constants import *


def filter_by_regular_hours(data, datetime_column):
    return data[(data[datetime_column].dt.time >= REGULAR_TRADING_HOURS_START) & \
                (data[datetime_column].dt.time <= REGULAR_TRADING_HOURS_END) & \
                (data[datetime_column].dt.dayofweek < 5)].reset_index(drop=True)