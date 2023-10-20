from quantfinance.Utils import Utilities as utils
import datetime
import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.filterwarnings("ignore")

def compute_signals(data, stock_name, rolling_period=14):
    if 'return' not in data:
        data['return'] = np.log(data[stock_name] / data[stock_name].shift(1))
    data['move'] = data[stock_name] - data[stock_name].shift(1)
    data['up'] = np.where(data['move'] > 0, data['move'] , 0)
    data['down'] = np.where(data['move'] < 0, data['move'], 0)
    data['average_gain'] = data['up'].rolling(rolling_period).mean()
    data['average_loss'] = data['down'].abs().rolling(rolling_period).mean()
    relative_strength = data['average_gain'] / data['average_loss']
    data['rsi'] = 100.0 -(100.0 / (1.0 + relative_strength))
    return data

def plot_signals(data, stock_ticker):
    plt.plot(data['rsi'])
    plt.xlabel('time')
    plt.ylabel('RSI')
    plt.axhline(y=70, color='r', linestyle='-')
    plt.axhline(y=30, color='r', linestyle='-')
    plt.title('Relative Strength Indicator for {}'.format(stock_ticker))
    plt.show()

if __name__ == "__main__":
    start = datetime.datetime(2022,1,1)
    end = datetime.datetime(2023,10,1)
    stock_ticker = 'JPM'
    ticker = [stock_ticker]
    data = utils.download_data(ticker, start, end)
    data = compute_signals(data, stock_ticker)
    data = data.dropna()
    plot_signals(data,stock_ticker)
