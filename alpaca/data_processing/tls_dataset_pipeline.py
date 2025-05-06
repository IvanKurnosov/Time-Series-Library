from data_retrieving import StockDataRetriever
from data_preprocessing_utils import *
from alpaca.feature_engineering import *

from datetime import datetime


def run():
    retriever = StockDataRetriever(
        start=datetime(2024, 9, 1),
        end=datetime(2025, 3, 1),
    )

    all_features = []
    stock_list = SNP500_STOCKS_SELECTED
    for i, symbol in stock_list:
        print(f'Retrieving {i}-th symbol out of {len(stock_list)}...')

        data = retriever(symbol)
        data = filter_by_regular_hours(data, TSLDatasetConstants.DATETIME_COLUMN_NAME)
        all_features.append(prepare_data_for_tsl_indicators(data, symbol, mode='train'))

    all_features = pd.concat(all_features, ignore_index=True)
    all_features.to_csv('data/dataset/sp500_symbols_2month.csv', index=False)




