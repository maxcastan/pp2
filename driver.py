import requests
import sys,os
from iex import Stock
import lxml.html
import sqlite3
import csv
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plot
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
'exec(%matplotlib inline)'

class Tickers:
    def save_tickers(self, n):
        '''
        Args:
            n: number of tickers to print to file
        '''
        fopen=open(sys.argv[2],'w+') #open the file in append mode
        page = requests.get('http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&pagesize=200') #saves all url info
        doc = lxml.html.fromstring(page.content)
        table = doc.xpath('//div[@class = "genTable thin"]')[0] #grabs first instance of genTable, which stores tickers
        unparsed_ticks = []
        for i in range(0,n):
            h3 = table.xpath('.//h3')[i]    #grabs all h3 headers
            ticks = h3.xpath('.//a')        #grabs a headers under h3
            for tick in ticks:
                unparsed_ticks.append(tick.text_content())      #includes a bunch of tabs
        total_ticks =[]
        for x in unparsed_ticks:
            total_ticks.append(x[-5:])      #removes tabs
        for x in total_ticks:
            sys.stdout = open(os.devnull,"w")   #suppresses stdout
            if(check_if_valid(self, x.strip())):
                print(x.strip(),file =fopen)        #prints list of tickers to file tickers.txt
            else:
                continue
            sys.stdout = sys.__stdout__
        fopen.close()

    def check_if_valid(self, ticker):
        '''
        uses iex-api-python to check if ticker has valid price function
        Args:
            ticker: fetched ticker from NASDAQ website
        '''
        try:
            price = Stock(ticker).price()
            if price:
                return True
            else:
                return False
        except(Exception,TypeError):
            return False


if __name__=="__main__":
    x=sys.argv[1]
    if(x=="Ticker"):
        ticker_count=sys.argv[2]
        print(ticker_count)
    elif(x=="Fetcher"):
        ticker_count=sys.argv[2]
        time_limit=sys.argv[3]
        db=sys.argv[4]
    elif(x=="Query"):
        time=sys.argv[2]
        db=sys.argv[3]
        ticker=sys.argv[4]
    else:
        print("Indicate Flag")
