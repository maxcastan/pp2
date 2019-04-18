from stock import Tickers
from stock import Fetcher
from stock import Query
import datetime

def test_ticker():
    t = Tickers(10)
    assert t.ticker == 'x'
    assert t.ticker_count == 10
    assert t.check_if_valid() == True
    

def test_fetcher():
    current_time = str(datetime.datetime.now())
    current_time = current_time[11::16]
    f = Fetcher(10,"test.db",30)
    f.fetch_all_data()
    q = Query(current_time,"test.db",'YI')
    assert q.get_data() != None
    


def test_query():
    q = Query('16:32',"stocks.db",'YI')
    assert q.time == '16:32'
    assert q.db == "stocks.db"
    assert q.ticker == 'YI'
    list1=[('16:32', 'YI', '5.82', '6.58', '5.82', '6.49', '6.49', '31101')]
    out1 = q.get_data()
    assert list1 == out1

        