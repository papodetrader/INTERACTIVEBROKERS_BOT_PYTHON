from execution import trading_execution
from plan import build_plan

import os
import datetime as dt
import pandas as pd
import pytz
import warnings
warnings.filterwarnings("ignore")


def read_variables():
    try:
        plan = [i for i in os.listdir('./DATA/plan/') if str(dt.datetime.now(tz=pytz.timezone('Europe/Moscow')).date()) in i][0]
        plan = pd.read_pickle(f'./DATA/plan/{plan}')
    except:
        build_plan().run_daily()
        plan = [i for i in os.listdir('./DATA/plan/') if str(dt.datetime.now(tz=pytz.timezone('Europe/Moscow')).date()) in i][0]
        plan = pd.read_pickle(f'./DATA/plan/{plan}')

    try:
        trades = [i for i in os.listdir('./DATA/trades/') if str(dt.datetime.now(tz=pytz.timezone('Europe/Moscow')).date()) in i][0]
        trades = pd.read_pickle(f'./DATA/trades/{trades}')

    except:
        trades = {}

    try:
        orders = [i for i in os.listdir('./DATA/orders/') if str(dt.datetime.now(tz=pytz.timezone('Europe/Moscow')).date()) in i][0]
        orders = pd.read_pickle(f'./DATA/orders/{orders}')
    except:
        orders = {}

    if len(orders.keys()) > 0:
        orders_ = pd.DataFrame(orders.values(), orders.keys()).index.value_counts()
        for i in range(len(orders_)):
            if orders_.index[i] in plan.keys():
                plan.get(orders_.index[i]).update({'try_qty': plan.get(orders_.index[i])['try_qty']-orders_.iloc[i]})

    if len(trades.keys()) > 0:
        trades_ = pd.DataFrame(trades.values(), trades.keys())
        trades_ = trades_[trades_.entry_date == dt.datetime.now(tz=pytz.timezone('Europe/Moscow')).date()]
        trades = pd.DataFrame.to_dict(trades_, orient='index')
        trades_ = trades_.set_index('plan_key').index.value_counts()
#         trades_ = pd.DataFrame(trades.values(), trades.keys()).set_index('plan_key').index.value_counts()
        for i in range(len(trades_)):
            if trades_.index[i] in plan.keys():
                plan.get(trades_.index[i]).update({'try_qty': plan.get(trades_.index[i])['try_qty']-trades_.iloc[i]})

    return plan, orders, trades


plan, orders, trades = read_variables()
execution = trading_execution(plan, orders, trades)


