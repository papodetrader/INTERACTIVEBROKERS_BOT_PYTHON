import time
import datetime as dt
import pandas as pd
import pytz


########################

# df = pd.read_pickle('./../DATA/IB')
# df_ind = pd.read_pickle('./../DATA/IB_OHLC')
plan = pd.read_pickle('./DATA/plan/plan_2019-08-26')
# plan = pd.DataFrame(plan.values(), plan.keys())
orders = pd.read_pickle('./DATA/orders/orders_2019-08-26')
# orders = pd.DataFrame(orders.values(), orders.keys())
# trades = pd.read_pickle('./DATA/trades/trades_2019-08-26')
# trades = pd.DataFrame(trades.values(), trades.keys())


# df = df.loc[df.asset.isin(['EURUSD', 'EURAUD', 'GBPCAD', 'USDCAD', 'USDJPY', 'AUDJPY', 'GBPJPY', 'IBDE30',
#  'IBGB100', 'IBFR40', 'IBJP225', 'IBHK50', 'IBUS500', 'IBUST100', 'IBAU200'])]

print(orders.keys())