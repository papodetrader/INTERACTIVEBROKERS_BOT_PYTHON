import pandas as pd
import numpy as np
import pickle
import ta

class ind:

    def __init__(self):
        pass

#################################################################################################

    def _indicadores(self, df):
        ''' ESTA FUNCAO NAO E EXECUDA, ELA EXECUTA ATRAVES DA FUNCAO INDICADOR() '''

        import warnings
        warnings.filterwarnings("ignore", message="divide by zero encountered in double_scalars")
        warnings.filterwarnings("ignore", message="invalid value encountered in double_scalars")

        db = pd.DataFrame()

        for i in df.asset.unique():

            df1 = df[df['asset'] == i].copy()
            df1['PD_low'] = df1.low.shift(1)
            df1['PD_high'] = df1.high.shift(1)
            df1['Change%'] = df1.close.pct_change().round(4)

            df1['SMA20'] = df1.close.rolling(20).mean().round(5)
            df1['SMA200'] = df1.close.rolling(200).mean().round(5)

            df1['ATR'] = ((df1.high - df1.low).rolling(10).mean() * 5 +
                        (df1.high - df1.low).rolling(60).mean() * 3 +
                        (df1.high - df1.low).rolling(1200).mean() * 2) / 10

            df1['M1_low'] = df1.low.resample('30D').min().reindex(df1.index, method='ffill')
            df1['M1_high'] = df1.high.resample('30D').max().reindex(df1.index, method='ffill')

            df1['RSI_5K'] = ta.stoch(df.high, df.low, df.close, 5).round(0) #FIXED
            df1['RSI_5D'] = ta.stoch_signal(df.high, df.low, df.close, 5, 3).round(0) #FIXED


            df1['d30%'] = ((df1.close - df1.close.shift(30)) / df1.close).round(4)


            db = pd.concat([db, df1])
            
        return db
   
    
#################################################################################################

    def indicador(self, df):
        from multiprocessing import Pool, cpu_count
        num_process = 2* cpu_count()
        
        with Pool(num_process) as pool:
            seq = [df[df['asset'] == i] for i in df.asset.unique()]

            results_list = pool.map(self._indicadores, seq)

            db = pd.concat(results_list)
            pd.DataFrame.sort_index(db, inplace=True)
        
            with open('./../DATA/IB_OHLC', 'wb') as f:
                pickle.dump(db, f, protocol=pickle.HIGHEST_PROTOCOL)    

            # print(db.tail())



