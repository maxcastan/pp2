'''
    command to run->python3 tickers.py numtickers tickers.txt
    py file to extract valid tickers from nasdaq website
    authors: Paulina Scarlata and Max Castaneda
'''
import requests
import sys,os
from iex import Stock
import lxml.html

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

def next_page(doc):
    '''
    code to switch url to next page-not used
    '''
    nextpage = doc.xpath('//div[@id="main_content_pagesizelist"]')[0]
    href = nextpage.xpath('//ul[@class="pager"]/li/a')[0]
    newurl = href.attrib['href']
    page =  requests.get(newurl)
    doc = lxml.html.fromstring(page.content)
    table = doc.xpath('//div[@class = "genTable thin"]')[0]
    return table

if __name__ ==  "__main__":
    save_tickers(int(sys.argv[1]))

'''
#this was another option to "click" the 200 items per page option but it didnt work
for option in options.xpath('//select/option'):
    if option.attrib['value']=="50":
        del option.attrib['selected']
    if option.attrib['value']=="200":
        option.attrib['selected']="selected"
    #print(option.attrib)
'''
