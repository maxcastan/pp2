from stock import Tickers
from stock import Fetcher
from stock import Query
import datetime
from datetime import datetime

def test_ticker():
    t = Tickers(10)
    assert t.ticker == 'x'
    assert t.ticker_count == 10
    assert t.check_if_valid() == True
    

def test_fetcher():
    f = Fetcher(10,'test.db',10)
    assert f.ticker_count == 10


def test_query():
    