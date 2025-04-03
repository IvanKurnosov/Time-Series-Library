API_KEY = "PKGG13YXB1TNOXBQC6UU"
API_SECRET = "DOrUyg0g639FRkLhNrKzQKVilmGvzg3PZCpyFpeK"

from alpaca.data.live import StockDataStream
from alpaca.data.enums import DataFeed
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest

import time
import asyncio

from data_processing.constants import SNP500_STOCKS


wss_client = StockDataStream(
    API_KEY,
    API_SECRET,
    feed=DataFeed.SIP
)

quote_client = StockHistoricalDataClient(
    API_KEY,
    API_SECRET,
)

quote_request_params = StockLatestQuoteRequest(
    symbol_or_symbols=SNP500_STOCKS,
    feed=DataFeed.SIP
)



# start_time = time.time()
# quotes = quote_client.get_stock_latest_quote(quote_request_params)
# print(quotes)
# print(f'request took {time.time() - start_time} seconds.')

class BarsResponseHandler:
    def __init__(self):
        self.debounce_timer = None
        self.debounce_delay = 1.

        # initializes bars data storage

    async def handle(self, data):
        if self.debounce_timer:
            self.debounce_timer.cancel()  # cancel previously scheduled check for last event

            try:
                await self.debounce_timer
            except asyncio.CancelledError:
                pass

        self.process_data(data)

        # Schedule a fresh debounce callback (new "last event" timer)
        self.debounce_timer = asyncio.create_task(self.identify_last_event())

    def process_data(self, data):
        # store data in a format suitable for model predicting
        print('     Not yet...')
        pass

    async def identify_last_event(self):
        try:
            await asyncio.sleep(self.debounce_delay)
            # No new events received within debounce_delay, trigger processing
            self.perform_trading_cycle()
        except asyncio.CancelledError:
            pass

    def perform_trading_cycle(self):
        """
        1. sell all stocks that where bought
        2. make sure that last handle_data_update call happened not recently
            - return otherwise
        3. get all stocks with enough history
            - return if there are none of them
        4. make sure that
        """
        print('Starting trading cycle!')

        pass

bars_response_handler = BarsResponseHandler()


async def bars_handler(data):
    await bars_response_handler.handle(data)

wss_client.subscribe_bars(bars_handler, *SNP500_STOCKS)
wss_client.run()