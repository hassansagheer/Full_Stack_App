from celery import shared_task
import yfinance as yf
from yahoo_fin.stock_info import *
from io import StringIO
import pandas as pd
import requests
import queue
from threading import Thread

@shared_task(bind = True)
def update_stock(self, stockpicker):
    try:
        details = {}
        available_stocks = tickers_nifty50()
        
        for i in stockpicker:
            if i in available_stocks:
                pass
            else:
                stockpicker.remove(i)

        n_threads = len(stockpicker)
        thread_list = []
        que = queue.Queue()
        
        for i in range(n_threads):
            thread = Thread(target = lambda q, arg1: q.put({stockpicker[i]: get_stock_data(arg1)}), args = (que, stockpicker[i]))
            thread_list.append(thread)
            thread_list[i].start()

        for thread in thread_list:
            thread.join()

        while not que.empty():
            data = que.get()
            details.update(data)
        
        return 'Done'
    except Exception as e:
        print(f"An error occurred: {e}")


def tickers_nifty50():
    site = "https://finance.yahoo.com/quote/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(site, headers=headers)
    html_content = response.text
    
    # Wrap the HTML content in a StringIO object
    table = pd.read_html(StringIO(html_content))[0]
    
    # Extract the tickers from the table
    tickers = table['Symbol'].tolist()
    return tickers

def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    stock_info = stock.info
    stock_history = stock.history(period='1d')
    stock_history_dict = stock_history.reset_index().to_dict(orient='records')
    return {'info': stock_info, 'history': stock_history_dict}