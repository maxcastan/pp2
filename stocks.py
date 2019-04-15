import requests
import sys,os
from iex import Stock
import lxml.html
import sqlite3
import csv
import pandas as pd
import numpy as np
from datetime import datetime
import datetime
import matplotlib.pyplot as plot
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
'exec(%matplotlib inline)'

class Tickers:
    def __init__(self, ticker_count):
        self.ticker_count=int(ticker_count)
        self.ticker='x'
    def save_tickers(self):
  
        fopen=open('tickers.txt','w+') #open the file in append mode
        page = requests.get('http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&pagesize=200') #saves all url info
        doc = lxml.html.fromstring(page.content)
        table = doc.xpath('//div[@class = "genTable thin"]')[0] #grabs first instance of genTable, which stores tickers
        unparsed_ticks = []
        for i in range(0, self.ticker_count):
            h3 = table.xpath('.//h3')[i]    #grabs all h3 headers
            ticks = h3.xpath('.//a')        #grabs a headers under h3
            for tick in ticks:
                unparsed_ticks.append(tick.text_content())      #includes a bunch of tabs
        total_ticks =[]
        for x in unparsed_ticks:
            total_ticks.append(x[-5:])      #removes tabs
        for x in total_ticks:
            sys.stdout = open(os.devnull,"w")   #suppresses stdout
            self.ticker=x.strip()
            if(self.check_if_valid()):
                print(x.strip(),file =fopen)        #prints list of tickers to file tickers.txt
            else:
                continue
            sys.stdout = sys.__stdout__
        fopen.close()

    def check_if_valid(self):
        try:
            price = Stock(self.ticker).price()
            if price:
                return True
            else:
                return False
        except(Exception,TypeError):
            return False

class Fetcher:
    def __init__(self, ticker_count, db, time_limit):
        self.ticker_count=ticker_count
        self.db=db
        self.time_limit=time_limit
    def addSecs(self, tm, secs):
        date=datetime.datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
        date=date+datetime.timedelta(seconds=secs)
        return date.time()

    def update_stock_info(self, ticker, stop):
        now=datetime.datetime.now()
        if(now.time()>stop):
                    sys.exit()

        conn=sqlite3.connect(self.db)
        c=conn.cursor()

        sys.stdout = open(os.devnull,"w")
        c.execute('INSERT INTO data(Time, Ticker, latestPrice, latestVolume, Close, Open, low, high) VALUES(?, ?, ?, ?, ?, ?, ?, ?)', (str(now.strftime("%H:%M")), str(ticker), str(Stock(ticker).quote().get('latestPrice')), str(Stock(ticker).quote().get('latestVolume'))
            , str(Stock(ticker).quote().get('close')), str(Stock(ticker).quote().get('open')), str(Stock(ticker).quote().get('low'))
            , str(Stock(ticker).quote().get('high'))))
        conn.commit()

        c.close()
        conn.close()
 
        sys.stdout = sys.__stdout__

    def fetch_all_data(self):
        conn=sqlite3.connect(self.db)
        c=conn.cursor()

        c.execute('CREATE TABLE IF NOT EXISTS data(Time VARCHAR, Ticker VARCHAR, latestPrice , latestVolume VARCHAR, Close VARCHAR, Open VARCHAR, low VARCHAR, high VARCHAR)')
        c.close()
        conn.close()
        present=datetime.datetime.now()
        stopTime=self.addSecs(present, int(self.time_limit))

        with open('tickers.txt',"r") as f:
            for tick in f:
                self.update_stock_info(tick.strip(), stopTime)

class Query:
    def __init__(self, time, db, ticker):
        self.time=time
        self.db=db
        self.ticker=ticker
    def print_data(self):
        conn=sqlite3.connect(self.db)
        c=conn.cursor()       
        
        c.execute('SELECT * FROM data WHERE Time=? AND Ticker=?', (self.time, self.ticker))
        rows=c.fetchall()
        print("(Time, Ticker, latestPrice, latestVolume, Close, Open, low, high)")
        for row in rows:
            print(row)

        c.close()
        conn.close()

if __name__=="__main__":
    x=sys.argv[1]
    if(x=="Ticker"):
        p=Tickers(sys.argv[2])
        p.save_tickers()
    elif(x=="Fetcher"):
        p=Fetcher(sys.argv[2], sys.argv[4], sys.argv[3])
        p.fetch_all_data()
    elif(x=="Query"):
        p=Query(sys.argv[2], sys.argv[3], sys.argv[4])
        p.print_data()
    else:
        print("Indicate Flag")
