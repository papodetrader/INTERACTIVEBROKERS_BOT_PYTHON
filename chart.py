import pandas as pd
import matplotlib.pyplot as plt
import handle_data as hd
from mpl_finance import candlestick2_ohlc
import os


def chart(plan, id, symbol, time, date): #UP-

        name = id + "_" + str(time)

        total = 0

        lt = []
        for i in plan.keys():
                if i == id:
                        for ii in plan.get(i)['strat'].keys():
                                
                                if plan.get(i)['strat'][ii] in lt:
                                        pass

                                else:
                                        lt.append(plan.get(i)['strat'][ii])
                                        total += 1

                                        df = hd.handler().candle_data(symbol, plan.get(i)['strat'][ii], 20)

                                        fig, ax = plt.subplots(figsize=(15,10))
                                        candlestick2_ohlc(ax, df.open, df.high, df.low, df.close, width=0.5, colorup='g', colordown='r')
                                        ax.set_title(f"{symbol} with {plan.get(i)['strat'][ii]} Minutes Candle",fontsize=18)
                                        
                                        if not os.path.exists(f'./DATA/charts/{date}'): #UP-
                                                os.makedirs(f'./DATA/charts/{date}') #UP-

                                        plt.savefig(f'./DATA/charts/{date}/{name}_{total}.svg') #UP-
                                        plt.clf()


