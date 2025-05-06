import pandas as pd
import numpy as np
from enum import Enum


class EMA:
    def __init__(self, period, base_feature='close'):
        self.period = period
        self.base_feature = base_feature

    def __call__(self, df):
        return df[self.base_feature].ewm(span=self.period, adjust=False).mean()


class RSI:
    def __init__(self, period=14, base_feature='close'):
        self.period = period
        self.base_feature = base_feature

    def __call__(self, df):
        delta = df[self.base_feature].diff()

        # Separate gains and losses
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        # Calculate the average gains and losses
        avg_gain = gain.rolling(window=self.period, min_periods=1).mean()
        avg_loss = loss.rolling(window=self.period, min_periods=1).mean()

        # Use Wilder's method for smoothing
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi


class MACD:
    def __init__(self, base_feature='close'):
        self.base_feature = base_feature

    def __call__(self, df):
        short_ema = df[self.base_feature].ewm(span=12, adjust=False).mean()
        long_ema = df[self.base_feature].ewm(span=26, adjust=False).mean()

        # Calculate the MACD Line
        macd = short_ema - long_ema

        # Calculate the Signal Line
        signal_line = macd.ewm(span=9, adjust=False).mean()

        # Calculate the MACD Histogram
        return macd - signal_line


class BollingerBand:
    class BBType(Enum):
        LOWER = 1
        UPPER = 2

    def __init__(self, bb_type: BBType, period=20, base_feature='close'):
        self.period = period
        self.bb_type = bb_type
        self.base_feature = base_feature

    def __call__(self, df):
        sma = df[self.base_feature].rolling(window=self.period).mean()

        # Calculate the rolling standard deviation
        std = df[self.base_feature].rolling(window=self.period).std()

        # Calculate the Bollinger Bands
        if self.bb_type == self.BBType.LOWER:
            return sma - (std * 2)
        else:
            return sma + (std * 2)


class VWAP:
    def __init__(self,
                 high_feature='high',
                 low_feature='low',
                 close_feature='close',
                 volume_feature='volume'):
        self.high_feature = high_feature
        self.low_feature = low_feature
        self.close_feature = close_feature
        self.volume_feature = volume_feature

    def __call__(self, df):
        typical_price = (df[self.high_feature] + df[self.low_feature] + df[self.close_feature]) / 3

        # Calculate Cumulative TPV and Cumulative Volume
        cumulative_tvp = (typical_price * df[self.volume_feature]).cumsum()
        cumulative_volume = df[self.volume_feature].cumsum()

        # Calculate the VWAP
        return cumulative_tvp / cumulative_volume


class Oscillator:
    class LineType(Enum):
        K = 1
        D = 2

    def __init__(self,
                 line_type: LineType,
                 period=14,
                 high_feature='high',
                 low_feature='low',
                 close_feature='close'):
        self.period = period
        self.line_type = line_type
        self.high_feature = high_feature
        self.low_feature = low_feature
        self.close_feature = close_feature

    def __call__(self, df):
        lowest_low = df[self.low_feature].rolling(window=self.period).min()
        highest_high = df[self.high_feature].rolling(window=self.period).max()

        k_line = ((df[self.close_feature] - lowest_low) / (highest_high - lowest_low)) * 100
        if self.line_type == self.LineType.K:
            # Calculate the %K Line
            return k_line
        else:
            # Calculate the %D Line
            return k_line.rolling(window=3).mean()


class ATR:
    def __init__(self,
                 period,
                 high_feature='high',
                 low_feature='low',
                 close_feature='close'):
        self.period = period
        self.high_feature = high_feature
        self.low_feature = low_feature
        self.close_feature = close_feature

    def __call__(self, df):
        # Calculate the True Range (TR)
        prev_close = df[self.close_feature].shift(1)

        temp_df = pd.DataFrame()
        temp_df['high-low'] = df[self.high_feature] - df[self.low_feature]
        temp_df['high-Previous close'] = np.abs(df[self.high_feature] - prev_close)
        temp_df['low-Previous close'] = np.abs(df[self.low_feature] - prev_close)

        tr = temp_df[['high-low', 'high-Previous close', 'low-Previous close']].max(axis=1)

        # Calculate the ATR using an Exponential Moving Average (EMA)
        return tr.ewm(span=self.period, adjust=False).mean()


class FRL:
    FIB_RATIOS = (0.236, 0.382, 0.500, 0.618, 0.764)

    def __init__(self,
                 fib_ratio,
                 period=10,
                 high_feature='high',
                 low_feature='low',
                 close_feature='close'):
        self.fib_ratio = fib_ratio
        self.period = period
        self.high_feature = high_feature
        self.low_feature = low_feature
        self.close_feature = close_feature

    def __call__(self, df):
        swing_high = df[self.high_feature].rolling(window=self.period).max()
        swing_low = df[self.low_feature].rolling(window=self.period).min()

        # Calculate Fibonacci levels
        return swing_low + (swing_high - swing_low) * self.fib_ratio


class Vol:
    def __init__(self,
                 period,
                 close_feature='close'):
        self.period = period
        self.close_feature = close_feature

    def __call__(self, df):
        prev_close = df[self.close_feature].shift(1)
        vol = abs(df[self.close_feature] - prev_close) / df[self.close_feature]
        return vol.ewm(span=self.period, adjust=False).mean().fillna(0)