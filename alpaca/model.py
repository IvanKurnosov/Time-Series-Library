import pickle
import time
import pandas as pd


class Model:
    def __init__(self, model_path='data_processing/models/lgb_spx_selected_6_mon.pkl'):
        with open(model_path, 'rb') as file:
            self.model = pickle.load(file)

    def predict_probabilities(self, stocks_features, start_time=None):
        if start_time:
            print(f'Model predicting started in {time.time() - start_time}')

        x = pd.concat(list(stocks_features.values()), axis=0).reset_index(drop=True).drop(['date'], axis=1).to_numpy()
        predictions = self.model.predict_proba(x)[:, 1]

        return {symbol: float(probability) for symbol, probability in zip(stocks_features.keys(), predictions)}

