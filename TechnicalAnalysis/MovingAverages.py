from quantfinance.Utils import Utilities as utils
import datetime
import matplotlib.pyplot as plt
import numpy as np

def compute_signals(data, stock_name, short_period=50, long_period=200):
    if 'return' not in data:
        data['return'] = np.log(data[stock_name] / data[stock_name].shift(1))
    data['Short SMA'] = data[stock_name].rolling(window=short_period).mean()
    data['Long SMA'] = data[stock_name].rolling(window=long_period).mean()
    data['Short EMA'] = data[stock_name].ewm(span=short_period,adjust=False).mean()
    data['Long EMA'] = data[stock_name].ewm(span=long_period, adjust=False).mean()
    return data

def plot_signals(data,stock_ticker):
    plt.figure(figsize=(12,6))
    plt.plot(data[stock_ticker],label='Stock Price', color='Black')
    plt.plot(data['Short SMA'], label='Short SMA', color='Red')
    plt.plot(data['Long SMA'], label='Long SMA', color='Green')
    plt.plot(data['Short EMA'], label='Short EMA', color='Orange')
    plt.plot(data['Long EMA'], label='Long EMA', color='Blue')
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.title("Moving Averages (MA) Indicators")
    plt.show()

if __name__ == "__main__":
    start = datetime.datetime(2022,1,1)
    end = datetime.datetime(2023,10,1)
    ticker = ['JPM']
    data = utils.download_data(ticker, start, end)
    print(data)
    data = compute_signals(data, 'JPM')
    data = data.dropna()
    print(data)
    plot_signals(data, 'JPM')




