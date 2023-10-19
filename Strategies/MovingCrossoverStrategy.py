import datetime
from algotrading.TechnicalAnalysis import MovingAverages as ma
from quantfinance.Utils import Utilities as utils
import matplotlib.pyplot as plt

class MovingAverageCrossingStrategy:

    def __init__(self, capital, stock, start_date, end_date, short_period=50, long_period=200):
        self.capital = capital
        self.market_value = [capital]
        self.stock = stock
        self.start_date = start_date
        self.end_date = end_date
        self.short_period = short_period
        self.long_period = long_period
        self.is_long = False
        self.data = None


    def run_strategy(self):
        self.data = utils.download_data([self.stock], start_date=self.start_date, end_date=self.end_date)
        self.data = ma.compute_signals(self.data, self.stock)
        purchase_price = 0
        for index, row in self.data.iterrows():
            date = index.strftime("%Y-%m-%d")
            if row['Short EMA'] < row['Long EMA'] and self.is_long:
                potential_new_market_value = (self.capital * row[self.stock] / purchase_price)
                pnl = potential_new_market_value - self.market_value[-1]
                if pnl > 0:
                    self.market_value.append(potential_new_market_value)
                    self.is_long = False
                    print("Actual Closed Position On {}: sold {} for ${:.2f} and bought for ${:.2f} and profit/loss is ${:.2f}".format(date,self.stock, row[self.stock], purchase_price, pnl))
                else:
                    print("Potential Closed Position On {} for loss: sold {} for ${:.2f} and bought for ${:.2f} and profit/loss is ${:.2f}".format(
                            date, self.stock, row[self.stock], purchase_price, pnl))
            elif row['Short EMA'] > row['Long EMA'] and not self.is_long:
                purchase_price = row[self.stock]
                self.is_long = True
                print("Opened Position On {}: bought {} at ${:.2f}".format(date,self.stock, purchase_price, ))

    def plot_market_value(self):
        print("Return so far: {:2f}".format(((self.market_value[-1] - self.market_value[0])/self.market_value[0])*100))
        plt.figure(figsize=(12,6))
        plt.title("Market Value of Portfolio")
        plt.plot(self.market_value, label="Market Value", color='Black')
        plt.xlabel('Date')
        plt.ylabel('Market Value')
        plt.show()

if __name__ == '__main__':
    start_date = datetime.datetime(2020,1,1)
    end_date = datetime.datetime(2023,10,19)
    strategy = MovingAverageCrossingStrategy(1e5, 'IWM',start_date, end_date)
    strategy.run_strategy()
    #print(strategy.market_value)
    strategy.plot_market_value()
