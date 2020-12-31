from pandas_datareader import data

from bot.BtStockTrader import BtStockTrader


def print_hi(name):
    print(f'Hi, {name}')


def run_bt_stock_trader():
    BtStockTrader().run()


if __name__ == '__main__':
    print_hi('PyCharm')
    run_bt_stock_trader()
