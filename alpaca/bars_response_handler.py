from trader import Trader
from repository import Repository

import asyncio
import time

class BarsResponseHandler:
    DEBOUNCE_DELAY = 1.
    MIN_DELAY_BETWEEN_TRADES = 30

    def __init__(self, trader: Trader, repository: Repository):
        self.trader = trader
        self.repository = repository

        self.debounce_timer = None
        self.last_trading_time = time.time() - 100


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
        self.repository.add_bar(data)

    async def identify_last_event(self):
        try:
            await asyncio.sleep(self.DEBOUNCE_DELAY)
            # No new events received within debounce_delay, trigger processing
            self.perform_trading_cycle()
        except asyncio.CancelledError:
            pass

    def perform_trading_cycle(self):
        try:
            print('Starting trading cycle!')
            trading_cycle_start_time = time.time()

            self.trader.close_all_deals()

            if time.time() - self.last_trading_time < self.MIN_DELAY_BETWEEN_TRADES:
                print("Attention! Performing trading after less than 30 seconds from the last one!")
                print(" Ending this trading cycle...")
                return

            stock_to_trade = self.trader.select_stock(start_time=trading_cycle_start_time)

            # buy stock_to_trade worth 100 USD

            self.repository.clean_recently_updated_symbols()

            trading_cycle_duration = time.time() - trading_cycle_start_time
            print(f'Trading cycle took {trading_cycle_duration} seconds!')

        except Exception as e:
            print(f'Exception occurred: {e}')