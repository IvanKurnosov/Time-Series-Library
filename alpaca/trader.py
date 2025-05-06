from repository import Repository

from model import Model
import time
import json


class Trader:
    ADDITIONAL_PROBABILITY = 0.1

    def __init__(self, model: Model, repository: Repository, predictions_to_probabilities_path='data_processing/models/preds_to_probabilities.json'):
        self.model = model
        self.repository = repository

        with open(predictions_to_probabilities_path, 'r') as json_file:
            self.predictions_to_probabilities = json.load(json_file)

    def select_stock(self, start_time=None):
        if start_time:
            print(f'Stock selection started in {time.time() - start_time}')

        stocks_features = self.repository.get_bars_features(start_time)
        model_probabilities = self.model.predict_probabilities(stocks_features, start_time)
        print(model_probabilities)
        grows_probabilities = self.calc_grows_probabilities(model_probabilities, start_time)
        print(grows_probabilities)

        transaction_costs = self.repository.get_transaction_costs(start_time)
        print(transaction_costs)
        volatility = self.repository.get_volatility(start_time)
        print(volatility)

        stocks_expected_returns = self.calculate_expected_returns(grows_probabilities, transaction_costs, volatility, start_time)
        print(stocks_expected_returns)
        print(max(list(stocks_expected_returns.values())))

        # return stock with max expected return
        return 'AAPL'

    def calc_grows_probabilities(self, model_probabilities, start_time=None):
        if start_time:
            print(f'Growth probability estimation started in {time.time() - start_time}')

        return {
            symbol: self.predictions_to_probabilities[str(int(prediction * 100) / 100)]
            for symbol, prediction in model_probabilities.items()
        }

    def calculate_expected_returns(self, grows_probabilities, transaction_costs, volatility, start_time=None):
        if start_time:
            print(f'Expected returns estimation started in {time.time() - start_time}')

        return {
            symbol: volatility[symbol] * (2 * (grows_probabilities[symbol] + self.ADDITIONAL_PROBABILITY) - 1) - transaction_costs[symbol]
            for symbol in grows_probabilities.keys()
        }

    def close_all_deals(self):
        # close all open position, so that everything is in cash

        pass

