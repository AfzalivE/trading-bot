import bt
import matplotlib.pyplot as plt
import pandas as pd
from os import path

NUM_DAYS = 500
LAST_DOWNLOAD = 'last_download'
DATE_FORMAT = "%Y-%m-%d"


class BtStockTrader(object):
    stocks = ['goog', 'tsla', 'aapl']
    csv_file_name = f'data/{"-".join(stocks)}.csv'
    if path.exists(csv_file_name):
        data = pd.read_csv(csv_file_name, parse_dates=["Date"]).set_index("Date")
    else:
        bt.get(stocks, start='2010-01-01').to_csv(csv_file_name)
        data = pd.read_csv(csv_file_name, parse_dates=["Date"]).set_index("Date")

    # print(data.index)
    data = data[data.index >= '2015-01-01']
    # data = data[data.index <= '2015-12-31']
    s1 = bt.Strategy('yearly', [bt.algos.RunYearly(),
                                bt.algos.SelectAll(),
                                bt.algos.WeighEqually(),
                                bt.algos.Rebalance()])

    s2 = bt.Strategy('monthly', [bt.algos.RunMonthly(),
                                 bt.algos.SelectAll(),
                                 bt.algos.WeighEqually(),
                                 bt.algos.Rebalance()])
    s = [s1, s2]

    def run(self):
        tests = []
        for strategy in self.s:
            test = bt.Backtest(strategy, self.data, initial_capital=10000)
            tests.append(test)
        res = bt.run(*tests)
        res.plot()
        res.display()
        plt.show()
