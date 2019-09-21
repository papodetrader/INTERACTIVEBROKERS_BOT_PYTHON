import pandas as pd
from indicat import indicators
from handle_data import handler
import datetime as dt



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
                elif i == 'strat5':
                    result.append(self.strategy5(id, 'strat5'))
                elif i == 'strat6':
                    result.append(self.strategy6(id, 'strat6'))
                elif i == 'strat7':
                    result.append(self.strategy7(id, 'strat7'))
                elif i == 'strat8':
                    result.append(self.strategy8(id, 'strat8'))


            res = [i[0] for i in result]
            strat = [i[1] for i in result]

            if 'False' in res:
                return 'False', strat

            return 'True', strat


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
                elif i == 'strat5':
                    result.append(self.strategy5(id, 'strat5'))
                elif i == 'strat6':
                    result.append(self.strategy6(id, 'strat6'))
                elif i == 'strat7':
                    result.append(self.strategy7(id, 'strat7'))
                elif i == 'strat8':
                    result.append(self.strategy8(id, 'strat8'))


            res = [i[0] for i in result]
            strat = [i[1] for i in result]

            if 'True' in res:
                return 'True', strat

            return 'False', strat



    def dataframe(self, id, strat, period=50):
    
        asset = self.plan[id]['asset']
        timeframe = self.plan[id]['strat'][strat]
        df = self.handle.candle_data(asset, timeframe, period+1)
        df = df.iloc[:-1]

        return df
    


    def strategy1(self, id, strat, period=5): 
        df = self.dataframe(id, strat, period+5)

        strat = self.indicators.rsi(df, period)


        if strat[1] < 30 and strat[0] > strat[1] and self.plan[id]['direction'] == 'buy':
            return 'True', (strat, df)

        elif strat[1] > 70 and strat[0] < strat[1] and self.plan[id]['direction'] == 'sell':
            return 'True', (strat, df)

        return 'False', (strat, df)



    def strategy2(self, id, strat, period=20):
        df = self.dataframe(id, strat, period+1)

        strat = self.indicators.MA(df, period)

        if df.iloc[-1].close > strat and self.plan[id]['direction'] == 'buy':
            return 'True', (strat, df)

        elif df.iloc[-1].close < strat and self.plan[id]['direction'] == 'sell':
            return 'True', (strat, df)

        return 'False', (strat, df)



    def strategy3(self, id, strat, period=20):
        df = self.dataframe(id, strat, period+1)
        
        strat = self.indicators.channel(df, period)

        if strat == 'long' and self.plan[id]['direction'] == 'buy':
            return 'True', (strat, df)

        elif strat == 'short' and self.plan[id]['direction'] == 'sell':
            return 'True', (strat, df)

        return 'False', (strat, df)