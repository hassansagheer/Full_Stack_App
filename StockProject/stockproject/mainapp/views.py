from django.shortcuts import render
import yfinance as yf
from yahoo_fin.stock_info import *
import pandas as pd
from django.http import HttpResponse
import time
from io import StringIO
import requests

# Create your views here.
def stockPicker(request):
    stock_picker = tickers_nifty50()
    print(stock_picker)
    return render(request, 'mainapp/stockpicker.html', {'stockpicker':stock_picker})

    

# def stockTracker(request):
#     try:
#         stockpicker = request.GET.getlist('stockpicker')
#         print(stockpicker)
#         details = {}
#         available_stocks = tickers_nifty50()
        
#         for i in stockpicker:
#             if i not in available_stocks:
#                 return HttpResponse("Error")
        
#         start = time.time()
#         for ticker in stockpicker:
#             # Fetch the stock data for each ticker
#             stock = yf.Ticker(ticker)
            
#             # Get detailed stock information
#             stock_info = stock.info
#             stock_history = stock.history(period='1d')
            
#             # Convert the data to a dictionary
#             stock_history_dict = stock_history.reset_index().to_dict(orient='records')
            
#             # Combine stock info and history
#             data = {
#                 'info': stock_info,
#                 'history': stock_history_dict
#             }
#             details[ticker] = data
        
#         end = time.time()
#         time_taken = end - start
#         print(time_taken)
        
#         print(details)
#         return render(request, 'mainapp/stocktracker.html', {'details': details})
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return render(request, 'mainapp/stocktracker.html', {'error': str(e)})







def stockTracker(request):
    try:
        stockpicker = request.GET.getlist('stockpicker')
        print(stockpicker)
        details = {}
        available_stocks = tickers_nifty50()
        
        for i in stockpicker:
            if i not in available_stocks:
                return HttpResponse("Error")
        
        start = time.time()
        for ticker in stockpicker:
            # Fetch the stock data for each ticker
            stock = yf.Ticker(ticker)
            
            # Get detailed stock information
            stock_info = stock.info
            stock_history = stock.history(period='1d')
            
            # Convert the data to a dictionary
            stock_history_dict = stock_history.reset_index().to_dict(orient='records')
            
            # Combine stock info and history
            data = {
                'info': stock_info,
                'history': stock_history_dict
            }
            details[ticker] = data
        
        end = time.time()
        time_taken = end - start
        print(time_taken)
        
        print(details)
        return render(request, 'mainapp/stocktracker.html', {'details': details})
    except Exception as e:
        print(f"An error occurred: {e}")
        return render(request, 'mainapp/stocktracker.html', {'error': str(e)})

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
