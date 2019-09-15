plan = {
    'EUR_USD_0': {
        atr = 0.00750
        break_lunch = [1100, 1500]
        trading_hours = [900, 1800]
        profit = [5, 30, 100, 'day']
        stop = [1.5, 30, 100, 'day']
        duration = pd.to_datetime(30, unit='m').time()
        try_qty = 3
        direction = 'sell'
        strat = {'strat2': 3}
        strat_cond = 'and'
        strat_name = 'trade_short'
        size = 100
    }, 

    'IBUS500': {
        atr = 18.00000
        break_lunch = [1100, 1500]
        trading_hours = [900, 1800]
        profit = [5, 30, 100, 'day']
        stop = [1.5, 30, 100, 'day']
        duration = pd.to_datetime(60, unit='m').time()
        try_qty = 3
        direction = 'sell'
        strat = {'strat1': 5}
        strat_cond = 'and'
        strat_name = 'trade_short'
        size = 100
    }
}