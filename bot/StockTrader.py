import dataclasses
from dataclasses import dataclass
from pandas_datareader import data
import pandas as pd
import pickledb
from datetime import date, datetime, timedelta
from random import random

NUM_DAYS = 500

LAST_DOWNLOAD = 'last_download'

DATE_FORMAT = "%Y-%m-%d"


@dataclass(frozen=True)
class Stock(object):
    symbol: str
    price: float
    quantity: int = 0


class StockTrader(object):
    data_source = 'yahoo'
    data_file = 'user_data.db'
    stocks = ['GOOG', "AAPL", "TSLA"]
    portfolio = {}
    cash = 20000

    def __init__(self):
        self.user_data = pickledb.load(self.data_file, auto_dump=True)

    def run(self):
        num_days = 0
        print(f'Start -- Cash: {self.cash}, portfolio: {self.portfolio}')
        start_date = '2018-01-02'
        while num_days < NUM_DAYS:
            today_date = datetime.strptime(start_date, DATE_FORMAT) + timedelta(days=num_days)
            # while True:
            for stock in self.stocks:
                # print(f"Reading stock data for {stock} on {today_date.strftime(DATE_FORMAT)}")
                df = pd.read_csv(f'data/{stock}.csv')
                one = df[df.Date == f'{today_date.strftime(DATE_FORMAT)}']
                if not one.empty:
                    closing_price = one['Close'].item()
                    if num_days == NUM_DAYS - 1:
                        print("Last day, selling everything")
                        self.sell_stock(Stock(symbol=stock, price=closing_price, quantity=99999))
                    elif num_days == 0:
                        self.purchase_stock(Stock(symbol=stock, price=closing_price, quantity=10))
                    else:
                        if random() < 0.5:
                            self.sell_stock(Stock(symbol=stock, price=closing_price, quantity=5))
                        else:
                            self.purchase_stock(Stock(symbol=stock, price=closing_price, quantity=10))

            num_days += 1

        print(f'End -- Cash: {self.cash}, portfolio: {self.portfolio}')
        pass

    def download_data(self):
        print("Downloading fresh data")
        for stock in self.stocks:
            data.DataReader(stock, data_source=self.data_source, start='2010-01-01', end='2020-12-30') \
                .to_csv(f'data/{stock}.csv')
        self.user_data.set(LAST_DOWNLOAD, date.today().strftime(DATE_FORMAT))
        pass

    def is_download_stale(self):
        last_download = self.user_data.get(LAST_DOWNLOAD)
        if not last_download:
            print('No last known download')
            return True
        delta_time = datetime.today() - datetime.strptime(last_download, DATE_FORMAT)
        print(f'Time since last download: {delta_time}')
        if delta_time.days > 10:
            print(f'More than 10 days since last download: {delta_time}')
            return True

        return False
        pass

    def purchase_stock(self, stock: Stock):
        order_price = stock.quantity * stock.price
        if self.cash < order_price:
            print("Ignoring purchase order, not enough cash")
            return

        print(f"Purchasing {stock.quantity} of {stock.symbol} @ {stock.price}")

        if self.portfolio.__contains__(stock.symbol):
            existing: Stock = self.portfolio[stock.symbol]
            new_quantity = existing.quantity + stock.quantity
            new_avg_price = (existing.price * existing.quantity + stock.price * stock.quantity) / new_quantity
            updated = Stock(symbol=stock.symbol, price=new_avg_price, quantity=new_quantity)
            self.portfolio[existing.symbol] = updated
        else:
            self.portfolio[stock.symbol] = stock

        self.cash = self.cash - order_price
        pass

    def sell_stock(self, stock: Stock):
        if self.portfolio.__contains__(stock.symbol):
            existing: Stock = self.portfolio[stock.symbol]
            sold_quantity = stock.quantity
            new_quantity = existing.quantity - sold_quantity
            if new_quantity < 0:
                new_quantity = 0
                sold_quantity = existing.quantity

            updated = Stock(existing.symbol, price=existing.price, quantity=new_quantity)
            if new_quantity > 0:
                self.portfolio[existing.symbol] = updated
            else:
                self.portfolio.pop(existing.symbol)

            print(f"Selling {sold_quantity} of {stock.symbol} @ {stock.price}")
            order_price = sold_quantity * stock.price
            self.cash = self.cash + order_price

    def sell_all(self):
        pass
