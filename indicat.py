import ta 
import pandas as pd
import numpy as np
from handle_data import handler

class indicators:
    
    def __init__(self):
        self.handle = handler()

    def ATR(self, df, period = 14, multiplier = 1):
        """ ATR bands input ATR(time = 14, multiplier = 1)."""
        
        df.columns = map(str.lower, df.columns) 
        df.sort_index(inplace = True)
        df = df.reset_index()
        z = ta.average_true_range(df['high'], df['low'], df['close'], period)
        z = z.iloc[-1]

        return float(z)*multiplier
  
    def MA(self, df, period = 14):
        
        df.columns = map(str.lower, df.columns) 
        df.sort_index(inplace = True)
        z = df.close.rolling(period).mean()
        z = z.iloc[-1]

        return round(float(z), 5)

#################################################################################################

    def rsi(self, df, period=5): 

        df.columns = map(str.lower, df.columns) 
        df.sort_index(inplace = True)
        df = df.reset_index() 

        rsi_k = ta.stoch(df['high'], df['low'], df['close'], period)
        rsi_k = rsi_k.iloc[-1]
        rsi_d = ta.stoch_signal(df['high'], df['low'], df['close'], period, 3)
        rsi_d = rsi_d.iloc[-1]

        return int(rsi_d), int(rsi_k)

