import pandas as pd
from indicat import indicators
from handle_data import handler



class strategy:
    
    def __init__(self, plan):
        self.handle = handler()
        self.indicators = indicators()
        self.plan = plan



    def master(self, id, cond= 'and'):
        result = []

        
        if cond == 'and':
            for i in self.plan[id]['strat'].keys():
                if i == 'strat1':
                    result.append(self.strategy1(id, 'strat1'))
                elif i == 'strat2':
                    result.append(self.strategy2(id, 'strat2'))
                elif i == 'strat3':
                    result.append(self.strategy3(id, 'strat3'))
                elif i == 'strat4':
                    result.append(self.strategy4(id, 'strat4'))

            if False in result:
                return False

            return True

        elif cond == 'or':
            for i in self.plan[id]['strat'].keys():
                if i == 'strat1':
                    result.append(self.strategy1(id, 'strat1'))
                elif i == 'strat2':
                    result.append(self.strategy2(id, 'strat2'))
                elif i == 'strat3':
                    result.append(self.strategy3(id, 'strat3'))
                elif i == 'strat4':
                    result.append(self.strategy4(id, 'strat4'))

            if True in result:
                return True

            return False



    def dataframe(self, id, strat, period=50):
    
        asset = self.plan[id]['asset']
        timeframe = self.plan[id]['strat'][strat]
        df = self.handle.candle_data(asset, timeframe, period+1)

        return df
    


    def strategy1(self, id, strat, period=3):
        
        return False
    


    def strategy2(self, id, strat, period=50): #UP-
        df = self.dataframe(id, strat, period)

        if self.indicators.rsi(df, period)[1] < 20 and self.indicators.rsi(df, period)[0] > self.indicators.rsi(df, period)[1] and self.plan[id]['direction'] == 'buy':
            return True

        elif self.indicators.rsi(df, period)[1] > 80 and self.indicators.rsi(df, period)[0] < self.indicators.rsi(df, period)[1] and self.plan[id]['direction'] == 'sell':
            return True

        return False



    def strategy3(self, id, strat, period=20):
        df = self.dataframe(id, strat, period)

        if df.iloc[-1].close > self.indicators.MA(df, period) and self.plan[id]['direction'] == 'buy':
            return True

        elif df.iloc[-1].close < self.indicators.MA(df, period) and self.plan[id]['direction'] == 'sell':
            return True

        return False



    def strategy4(self, id, strat, period=20):
        df = self.dataframe(id, strat, period)

        if self.indicators.channel(df, period) == 'long' and self.plan[id]['direction'] == 'buy':
            return True

        elif self.indicators.channel(df, period) == 'short' and self.plan[id]['direction'] == 'sell':
            return True

        return False



