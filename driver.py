from stock import *
import sys,os
import argparse

parser=argparse.ArgumentParser(description="Run program")
parser.add_argument('--operation', type=str, required=True)
parser.add_argument('--ticker_count', type=str)
parser.add_argument('--time_limit', type=str)
parser.add_argument('--db', type=str)
parser.add_argument('--time', type=str)
parser.add_argument('--ticker', type=str)
args=parser.parse_args()

if __name__=="__main__":
    x=args.operation
    if(x=="Ticker"):
        y=args.ticker_count
        print(y)
        p=Tickers(y)
        p.save_tickers()
    elif(x=="Fetcher"):
        y=args.ticker_count
        z=args.db
        v=args.time_limit
        p=Fetcher(y, z, v)
        p.fetch_all_data()
    elif(x=="Query"):
        y=args.time
        z=args.db
        v=args.ticker
        v=v.upper()
        p=Query(y, z, v)
        p.print_data()
    else:
        print("Indicate Flag")

