from celery import shared_task
import yfinance as yf
from yahoo_fin.stock_info import *
import pandas as pd
from django.http import HttpResponse
import time
from io import StringIO
import requests
import queue
from threading import Thread

@shared_task(bind = True)
def update(self, stockpicker):
    try:
        # stockpicker = request.GET.getlist('stockpicker')
        # print(stockpicker)
        details = {}
        available_stocks = tickers_nifty50()
        
        for i in stockpicker:
            if i not in available_stocks:
                return HttpResponse("Error")
        
        n_threads = len(stockpicker)
        thread_list = []
        que = queue.Queue()

        start = time.time()        
        for i in range(n_threads):
            thread = Thread(target = lambda q, arg1: q.put({stockpicker[i]: get_stock_data(arg1)}), args = (que, stockpicker[i]))
            thread_list.append(thread)
            thread_list[i].start()

        for thread in thread_list:
            thread.join()

        while not que.empty():
            data = que.get()
            details.update(data)

        end = time.time()
        time_taken = end - start
        print(time_taken)
        
        print(details)
    except Exception as e:
        print(f"An error occurred: {e}")