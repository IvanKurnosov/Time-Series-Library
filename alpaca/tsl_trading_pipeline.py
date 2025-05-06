API_KEY = "PKGG13YXB1TNOXBQC6UU"
API_SECRET = "DOrUyg0g639FRkLhNrKzQKVilmGvzg3PZCpyFpeK"

from alpaca.data.live import StockDataStream
from alpaca.data.enums import DataFeed

from constants import SNP500_STOCKS_SELECTED
from bars_response_handler import BarsResponseHandler
from quotes_response_handler import QuotesResponseHandler
from trader import Trader
from repository import Repository
from model import Model



wss_client = StockDataStream(
    API_KEY,
    API_SECRET,
    feed=DataFeed.SIP
)

trading_symbols = SNP500_STOCKS_SELECTED
repository = Repository(trading_symbols, API_KEY, API_SECRET)
model = Model()
trader = Trader(model, repository)
bars_response_handler = BarsResponseHandler(trader, repository)
quotes_response_handler = QuotesResponseHandler(repository)

async def bars_handler(data):
    await bars_response_handler.handle(data)

async def quotes_handler(data):
    await quotes_response_handler.handle(data)

wss_client.subscribe_bars(bars_handler, *trading_symbols)
wss_client.subscribe_quotes(quotes_handler, *trading_symbols)
wss_client.run()