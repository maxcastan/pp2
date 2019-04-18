from stock import *
import sys,os

if __name__=="__main__":
    x=sys.argv[1]
    if(x=="--operation=Ticker"):
        y=sys.argv[2]
        v=y[15:]
        p=Tickers(v)
        p.save_tickers()
    elif(x=="--operation=Fetcher"):
        y=sys.argv[2]
        z=sys.argv[4]
        v=sys.argv[3]
        a=y[15:]
        b=z[5:]
        c=v[13:]
        p=Fetcher(a, b, c)
        p.fetch_all_data()
    elif(x=="--operation=Query"):
        y=sys.argv[2]
        z=sys.argv[3]
        v=sys.argv[4]
        a=y[7:]
        b=z[5:]
        c=v[9:]
        p=Query(a, b, c)
        p.print_data()
    else:
        print("Indicate Flag")

