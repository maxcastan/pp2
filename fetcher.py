'''
    command to run->python3 fetcher.py time_lim tickers.txt info.csv
    this module updates stock information from a given ticker symbol
    authors: Paulina Scarlata and Max Castaneda

'''
import sys,os
from iex import Stock
import datetime

def addSecs(tm, secs):
    '''
        Args:
            tm: present times
            secs: how many second to run
    '''
    date=datetime.datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
    date=date+datetime.timedelta(seconds=secs)
    return date.time()

def update_stock_info(ticker, stop):
    '''
        Args:
            ticker: passed in single tickers
            stop: return value from addSecs
    '''
    now=datetime.datetime.now()

    if(now.time()>stop):
        sys.exit()
    sys.stdout = open(os.devnull,"w")
    print(now.strftime("%H:%M"), file=outfile, end=',')
    print(ticker,file = outfile,end =',')
    print(Stock(ticker).quote().get('latestPrice'),file =outfile,end=',')
    print(Stock(ticker).quote().get('latestVolume'),file =outfile,end=',')
    print(Stock(ticker).quote().get('close'),file =outfile,end=',')
    print(Stock(ticker).quote().get('open'),file =outfile,end=',')
    print(Stock(ticker).quote().get('low'),file =outfile,end=',')
    print(Stock(ticker).quote().get('high'),file =outfile)
    sys.stdout = sys.__stdout__

if __name__ == "__main__":
    cwd=os.getcwd()
    slash="/"
    path=cwd+slash+sys.argv[3]
    exists=os.path.isfile(path)
    outfile=open(sys.argv[3], "a")
    if not(exists):
        print("Time, Ticker, latestPrice, latestVolume, Close, Open, low, high", file=outfile)

    present=datetime.datetime.now()
    stopTime=addSecs(present, int(sys.argv[1]))

    with open(sys.argv[2],"r") as f:
        for tick in f:
            update_stock_info(tick.strip(), stopTime)
    outfile.close()
