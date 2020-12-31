from pandas_datareader import data

from bot.BtStockTrader import BtStockTrader
from bot.StockTrader import StockTrader


def print_hi(name):
    print(f'Hi, {name}')


def run_stock_trader():
    trader = StockTrader()
    if trader.is_download_stale():
        trader.download_data()
    trader.run()
    pass


def run_bt_stock_trader():
    BtStockTrader().run()


if __name__ == '__main__':
    print_hi('PyCharm')
    # run_stock_trader()
    run_bt_stock_trader()
