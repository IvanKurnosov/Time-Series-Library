import time
import json


from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.historical import StockHistoricalDataClient

from feature_engineering import prepare_data_for_tsl_indicators
from indicators import *


class Repository:
    BARS_COLUMNS = ["open", "high", "low", "close", "volume", "date"]
    BARS_DATA_DEPTH = 28
    VOLATILITY_CALCULATION_PERIOD = 10
    TRANSFORMATIONS_PATH = "data_processing/data/transformations/tsl_transformations_{0}.json"

    def __init__(self, trading_symbols, api_key, api_secret):
        self.symbols = trading_symbols
        self.recently_updated_symbols = []
        self.api_key = api_key
        self.api_secret = api_secret

        self.bars = self.initialize_bars_with_latest_values()
        self.transformations = self.initialize_feature_transformations()

        self.spreads = {symbol: 100 for symbol in trading_symbols}
        self.top_volumes_usd = {symbol: 0 for symbol in trading_symbols}

        self.volatility_calculator = Vol(period=self.VOLATILITY_CALCULATION_PERIOD)


    def initialize_bars_with_latest_values(self):
        print('Starting bars initialization...')

        bars = {}
        client = StockHistoricalDataClient(self.api_key, self.api_secret)
        request_params = StockBarsRequest(
            symbol_or_symbols=self.symbols,
            timeframe=TimeFrame.Minute,
            feed='sip',

        )
        all_stocks_df = client.get_stock_bars(request_params).df
        for stock in self.symbols:
            stock_df = all_stocks_df.xs(stock, level='symbol')
            stock_df = stock_df.assign(date=stock_df.index)
            stock_df = stock_df[self.BARS_COLUMNS]
            bars[stock] = stock_df.tail(self.BARS_DATA_DEPTH).reset_index(drop=True)

        print('Bars initialization finished!')

        return bars

    def initialize_feature_transformations(self):
        transformations = {}
        for symbol in self.symbols:
            with open(self.TRANSFORMATIONS_PATH.format(symbol), 'r') as file:
                transformations[symbol] = json.load(file)

        return transformations

    def add_bar(self, data):
        self.recently_updated_symbols.append(data.symbol)

        self.bars[data.symbol].loc[len(self.bars[data.symbol])] = {
            "open": data.open,
            "high": data.high,
            "low": data.low,
            "close": data.close,
            "volume": data.volume,
            "date": data.timestamp
        }

    def add_quote(self, data):
        self.spreads[data.symbol] = data.ask_price - data.bid_price
        self.top_volumes_usd[data.symbol] = data.ask_price * min(data.ask_size, data.bid_size)

    def get_bars_features(self, start_time=None):
        if start_time:
            print(f'Bars features calculation started in {time.time() - start_time}')

        bars_features = {}
        for symbol in self.recently_updated_symbols:
            bars_features[symbol] = prepare_data_for_tsl_indicators(self.bars[symbol], symbol, mode='test', transformations=self.transformations[symbol], verbose=False).tail(1)

        return bars_features

    def get_transaction_costs(self, start_time=None):
        if start_time:
            print(f'Transaction cost calculation started in {time.time() - start_time}')

        return {
            symbol: spread / float(self.bars[symbol]['close'].iloc[-1])
            for symbol, spread in self.spreads.items()
        }

    def get_volatility(self, start_time=None):
        if start_time:
            print(f'Volatility calculation started in {time.time() - start_time}')

        return {
            symbol: float(self.volatility_calculator(bars_df).iloc[-1])
            for symbol, bars_df in self.bars.items()
        }

    def clean_recently_updated_symbols(self):
        self.recently_updated_symbols.clear()