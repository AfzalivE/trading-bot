import simfin as sf
from simfin.names import *
import pandas as pd
import matplotlib.pyplot as plt


class Downloader(object):
    sf.set_api_key('free')
    sf.set_data_dir('simfin_data/')

    def download(self):
        # df = sf.load_derived(variant='quarterly', market='us')
        # print(df.loc['AAPL'])
        # df = sf.load_shareprices(variant='daily', market='us')
        # print(df.loc['AAPL'])
        df = sf.load_balance(variant='quarterly', market='us')
        # Get high and low share price for the quarter
        shares_df = sf.load_shareprices(variant='daily', market='us')
        aapl = shares_df.loc['AAPL']

        aapl = aapl.loc['2018-12-31':'2019-01-01', ADJ_CLOSE]
        print(aapl)
        # aapl = df.loc['AAPL', [TOTAL_ASSETS, TOTAL_LIAB]].pct_change()
        # aapl = df.loc['AAPL', [SHARES_DILUTED, LT_DEBT]]
        aapl.plot(grid=True, title="AAPL total assets")
        # plt.show()
