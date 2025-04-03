from indicators import *
from constants import *

import json


def prepare_data_for_tsl_indicators(data, symbol, mode="train", transformations_path='data/transformations/tsl_transformations_{0}.json'):
    if mode != 'train':
        with open(transformations_path.format(symbol), 'r') as file:
            transformations = json.load(file)

    features = data
    features[TSLDatasetConstants.DATETIME_COLUMN_NAME] = pd.to_datetime(features[TSLDatasetConstants.DATETIME_COLUMN_NAME], unit='ms')
    features['return'] = features['close'].pct_change()

    features['return_H'] = features['high'] / features['close'].shift(1) - 1
    features['return_L'] = features['low'] / features['close'].shift(1) - 1

    return_based_indicators = {
        "EMA_9": EMA(9, base_feature="return"),
        "EMA_12": EMA(12, base_feature="return"),
        "EMA_26": EMA(26, base_feature="return"),
        "MACD": MACD(base_feature="return"),
        "BB_LOW": BollingerBand(BollingerBand.BBType.LOWER, base_feature="return"),
        "BB_UP": BollingerBand(BollingerBand.BBType.UPPER, base_feature="return"),
        "VWAP": VWAP(high_feature='return_H', low_feature='return_L', close_feature='return'),
        "ATR_14": ATR(14, high_feature='return_H', low_feature='return_L', close_feature='return'),
        "ATR_28": ATR(28, high_feature='return_H', low_feature='return_L', close_feature='return'),
        "FRL_0": FRL(FRL.FIB_RATIOS[0], high_feature='return_H', low_feature='return_L', close_feature='return'),
        "FRL_1": FRL(FRL.FIB_RATIOS[1], high_feature='return_H', low_feature='return_L', close_feature='return'),
        "FRL_2": FRL(FRL.FIB_RATIOS[2], high_feature='return_H', low_feature='return_L', close_feature='return'),
        "FRL_3": FRL(FRL.FIB_RATIOS[3], high_feature='return_H', low_feature='return_L', close_feature='return'),
        "FRL_4": FRL(FRL.FIB_RATIOS[4], high_feature='return_H', low_feature='return_L', close_feature='return'),
    }

    zero_to_hundred_indicators = {
        "RSI_7": RSI(7),
        "RSI_14": RSI(14),
        "RSI_28": RSI(28),
        "Oscillator_K": Oscillator(Oscillator.LineType.K),
        "Oscillator_D": Oscillator(Oscillator.LineType.D),
    }

    if mode == 'train':
        return_mean = features['return'].mean()
        return_std = features['return'].std()
    else:
        return_mean = transformations['return']['mean']
        return_std = transformations['return']['std']

    for indicator_name, indicator_transformation in return_based_indicators.items():
        indicator_value = indicator_transformation(features)
        features[indicator_name] = (indicator_value - return_mean) / return_std
    features['return'] = (features['return'] - return_mean) / return_std

    for indicator_name, indicator_transformation in zero_to_hundred_indicators.items():
        features[indicator_name] = indicator_transformation(features) / 100

    if mode == 'train':
        volume_mean = features['volume'].mean()
        volume_std = features['volume'].std()
    else:
        volume_mean = transformations['volume']['mean']
        volume_std = transformations['volume']['std']

    features['volume'] = (features['volume'] - volume_mean) / volume_std

    if mode == 'train':
        with open(transformations_path.format(symbol), 'w') as file:
            transformations = {
                "return": {
                    "mean": return_mean,
                    "std": return_std
                },
                "volume": {
                    "mean": volume_mean,
                    "std": volume_std
                },
            }
            json.dump(transformations, file)

    numerical_feature_names = ['return', 'volume'] + list((return_based_indicators | zero_to_hundred_indicators).keys())
    features = features[[TSLDatasetConstants.DATETIME_COLUMN_NAME] + numerical_feature_names]
    features.loc[:, numerical_feature_names] = features.loc[:, numerical_feature_names].astype(np.float32)
    return features.reset_index(drop=True)
