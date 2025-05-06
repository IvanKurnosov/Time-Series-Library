from alpaca.constants import *

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime


class StockDataRetriever:
    API_KEY = "PKGG13YXB1TNOXBQC6UU"
    API_SECRET = "DOrUyg0g639FRkLhNrKzQKVilmGvzg3PZCpyFpeK"

    def __init__(self,
            start=datetime(2025, 1, 1),
            end=datetime(2025, 3, 1),
            timeframe=TimeFrame.Minute):
        self.start = start
        self.end = end
        self.timeframe = timeframe

    def __call__(self, symbol):
        client = StockHistoricalDataClient(self.API_KEY,  self.API_SECRET)

        request_params = StockBarsRequest(
            symbol_or_symbols=[symbol],
            timeframe=self.timeframe,
            start=self.start,
            end=self.end,
            feed='sip'
        )
        bars = client.get_stock_bars(request_params).df
        bars[TSLDatasetConstants.DATETIME_COLUMN_NAME] = [cur_index[1] for cur_index in bars.index]

        return bars.reset_index(drop=True)