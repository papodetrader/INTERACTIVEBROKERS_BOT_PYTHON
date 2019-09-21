import pandas as pd
import datetime as dt
from plan_indicat import ind
import pickle
from user_data import *
from handle_data import handler
import pytz
import os

import warnings
warnings.filterwarnings("ignore")

capital = float(handler().account_balance())
daily_risk = capital * MAX_PERCENTAGE_ACCOUNT_AT_RISK
ind = ind()

trade_short = [] 
trade_long = [] 

class build_plan:

    def __init__(self):
            self.handler = handler()
            self.assets = handler().assets
            self.assets_trade = ['EURUSD', 'EURAUD', 'GBPJPY', 'GBPCAD', 'USDCAD', 'USDJPY', 'AUDJPY',
                                    'IBUS500', 'IBUST100', 'IBGB100', 'IBDE30', 'IBFR40'] 
                                    #'IBJP225', 'IBAU200', 'IBHK50', 'XAUUSD', 'XAGUSD', 'EURSEK', 'CHFZAR', 'CHFNOK', 'CHFCNH'



    def _get_new_data(self):
            if 'IB' not in os.listdir('./../DATA/'):
                    last = dt.datetime.now(tz=pytz.timezone("Europe/Moscow")).date() - dt.timedelta(1900)
                    db = pd.DataFrame()
            else:
                    db = pd.read_pickle('./../DATA/IB') 
                    db.columns = db.columns.str.lower()
                    db = db[db.index < sorted(db.index.unique())[-1]]

                    db = db.reset_index().set_index('date')
                    last = sorted(db.index.unique())[-1].date()
                    

            data = pd.DataFrame()

            if last == (dt.datetime.now(tz=pytz.timezone("Europe/Moscow")).date()):
                    pass
            else:
                    total = int(str(dt.datetime.now(tz=pytz.timezone("Europe/Moscow")).date()-last).split(' ')[0])

                    for i in self.assets_trade: 
                            df = self.handler.candle_data(i, 1440, total) 

                            data = pd.concat([data, df], sort=True).drop_duplicates()

                    data = data.set_index(['date', 'asset'])

                    if len(db) > 1:
                            db = db.reset_index().set_index(['date', 'asset'])
                            data = pd.concat([db, data], sort=True).drop_duplicates()

                    
                    data = data.reset_index().set_index('date')


                    self._remove_duplicated(data)
            


    def _remove_duplicated(self, df):

            df = df.reset_index()
            db = pd.DataFrame()

            for i in df.asset.unique():
                    data = df[df.asset == i]      
                    pd.DataFrame.drop_duplicates(data, subset='date', inplace=True)  
                    db = pd.concat([db, data], sort=True)

            db = db.set_index('date')

            pd.DataFrame.sort_index(db, inplace=True)

            db = db[db.index.date < dt.datetime.now(tz=pytz.timezone("Europe/Moscow")).date()]
            db = db.dropna()

            db.to_pickle('./../DATA/IB') 

            db = db[db.asset.isin(self.assets_trade)]
            db = db[db.index.dayofweek < 5]



    def run_daily():
    
        plan = {
            'EUR_USD_0': {
                'atr' : 0.00750,
                'break_lunch' : [1100, 1500],
                'trading_hours' : [900, 1800],
                'profit' : [5, 30, 100, 'day'],
                'stop' : [1.5, 30, 100, 'day'],
                'duration' : pd.to_datetime(30, unit='m').time(),
                'try_qty' : 3,
                'direction' : 'sell',
                'strat' : {'strat2': 3},
                'strat_cond' : 'and',
                'strat_name' : 'trade_short',
                'size' : 100
                }, 

            'IBUS500': {
                'atr' : 18.00000,
                'break_lunch' : [1100, 1500],
                'trading_hours' : [900, 1800],
                'profit' : [5, 30, 100, 'day'],
                'stop' : [1.5, 30, 100, 'day'],
                'duration' : pd.to_datetime(60, unit='m').time(),
                'try_qty' : 3,
                'direction' : 'sell',
                'strat' : {'strat1': 5},
                'strat_cond' : 'and',
                'strat_name' : 'trade_short',
                'size' : 100
                }
            }

        pd.to_pickle(plan, f'./DATA/plan/plan_{dt.datetime.now(tz=pytz.timezone("Europe/Moscow")).date()}')


        return plan