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
    def save_tickers(n):
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
            if(check_if_valid(x.strip())):
                print(x.strip(),file =fopen)        #prints list of tickers to file tickers.txt
            else:
                continue
            sys.stdout = sys.__stdout__
        fopen.close()

    def check_if_valid(ticker):
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

class Fetcher:

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

class Query:

    def print_query_data(infofile,ticker,time, verbose):
        '''
            Args:
                infofile: info.csv file generated from fetcher.py
                ticker: single ticker name
                time: time to search for in info.csv file
                verbose: whether or not to include time/file info 
        '''
        with open(infofile) as csvfile:
            csvreader =  csv.reader(csvfile,delimiter=',')
            for row in csvreader:
                if (row[0]==time)and(row[1]==ticker):
                    if(verbose=='True'):
                        print("Time: "+time)
                        print("File: "+infofile)
                        print("Ticker: "+ ticker)
                    print("Latest Price: "+row[2])
                    print("Latest Volume: "+row[3])
                    print("Close: "+row[4])
                    print("Open: "+row[5])
                    print("Low: "+row[6])
                    print("High: "+row[7]+"\n\n")