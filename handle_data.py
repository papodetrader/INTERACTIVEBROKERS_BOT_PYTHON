import pandas as pd
import pytz
import datetime as dt
import decimal
from ib_insync import *
from assets import asset, assets
import time
from user_data import *


ib = IB()
ib.connect('127.0.0.1', 4002, clientId=clientID) #7496 TWS - 4002 GATEWAY

class handler:
    
    def __init__(self):
        self.assets = assets
        self.asset = asset
    


    def getGranularity(self, size_in_minutes):
            if size_in_minutes == 1:
                return "1 min"
            elif size_in_minutes == 5:
                return "5 mins"
            elif size_in_minutes == 15:
                return "15 mins"
            elif size_in_minutes == 30:
                return "30 mins"
            elif size_in_minutes == 60:
                return "1 hour"
            elif size_in_minutes == 120:
                return "2 hours"
            elif size_in_minutes == 240:
                return "4 hours"
            elif size_in_minutes == 480:
                return "8 hours"
            elif size_in_minutes == 1440:
                return "1 day"
            elif size_in_minutes == 10080:
                return "1 week"
            elif size_in_minutes == 43800:
                return "1 month"
            # default: two hour candles
            return "1 min"



    def candle_data(self, symbol, size_in_minutes, count, endDateTime=''):
        """ Candle data for symbols """
        
        contract = self.contract_find(symbol)
        
        count = (size_in_minutes * count * 60) +1

        if count < 86400:     
            count = str(count) + ' S'
        elif count > 86400 and count < 2592000:
            count = '30 D'
        elif count > 2592000 and count < 7862400:
            count = '13 W'
        elif count > 7862400:
            count = '10 Y'

        size_in_minutes = self.getGranularity(size_in_minutes)

        bars = ib.reqHistoricalData(contract, endDateTime=endDateTime, durationStr= count,
        barSizeSetting= size_in_minutes, whatToShow='MIDPOINT', useRTH=False)

        # convert to pandas dataframe:
        df = util.df(bars)[['date', 'open', 'high', 'low', 'close']]
        df['asset'] = symbol

        return df



    def contract_find(self, symbol): #UP
    
        type = [self.assets.get(i)[2] for i in self.assets.keys() if symbol in self.assets.get(i)[0]][0]
        exchange = [self.assets.get(i)[1] for i in self.assets.keys() if symbol in self.assets.get(i)[0]][0]

        
        if type == 'Forex':
            return Forex(symbol, exchange= exchange)
            
        elif type == 'CFD':
            return CFD(symbol, exchange= exchange)

        elif type == 'Future':
            localSymbol = ib.reqContractDetails(Future(symbol, exchange= exchange))[0].contract.localSymbol
            secType = ib.reqContractDetails(Future(symbol, exchange= exchange))[0].contract.secType
            conId = ib.reqContractDetails(Future(symbol, exchange= exchange))[0].contract.conId
            lastTraded = ib.reqContractDetails(Future(symbol, exchange= exchange))[0].contract.lastTradeDateOrContractMonth

            return Future(secType= secType, conId= conId, symbol= symbol, lastTradeDateOrContractMonth= lastTraded, exchange= exchange, localSymbol=localSymbol)

        elif type == 'CMDTY':
            return Commodity(symbol, exchange= exchange)
            
        elif type == 'Stock':
            return Stock(symbol, exchange= exchange)

    

    def order(self, symbol, size, target, stop, lmt=0, type='mkt'):

        action = 'BUY' if size > 0 else 'SELL'

        bracket = ib.bracketOrder(action= action, quantity= abs(size), limitPrice= lmt, takeProfitPrice= target, stopLossPrice= stop, tif='GTC', outsideRth=True) #UP
        bracket.parent.update(transmit = False)
        bracket.takeProfit.update(transmit = False)
        bracket.stopLoss.update(transmit = True)

        if type == 'mkt':
            bracket.parent.orderType = 'MKT'

        order = []
        for o in bracket:
            order.append(ib.placeOrder(self.contract_find(symbol), o))
            

        return order


    
    def open_positions(self):

        lmt = {}
        stp = {}

        for i in ib.openOrders():
            qty = i.totalQuantity if i.action == 'SELL' else -1*i.totalQuantity
            if i.orderType == 'LMT':
                lmt.update({i.ocaGroup: {'targetID': i.permId, 'target': i.lmtPrice, 'qty': qty}})
            elif i.orderType == 'STP':
                stp.update({i.ocaGroup: {'stopID': i.permId, 'stop': i.auxPrice}})

        lmt = pd.DataFrame(lmt.values(), lmt.keys())
        stp = pd.DataFrame(stp.values(), stp.keys())

        db = pd.concat([lmt, stp], axis=1, sort=True)

        lt = {}

        for i in ib.fills():
            if str(i.execution.permId) in db.index:
                lt.update({str(i.execution.permId): {'entry_price': i.execution.price, 'date': i.execution.time.date(), 
                                                    'asset': self.symbol_fix(i.contract.localSymbol), 'entry_time': (i.execution.time + dt.timedelta(hours=3)).time(),
                                                    'commission':i.commissionReport.commission, 'orderID': i.execution.orderId}})
            
        lt = pd.DataFrame(lt.values(), lt.keys())

        db = pd.concat([db, lt], axis=1, sort=True)

        return db.to_dict(orient='index')



    def account_balance(self):

        balance = float([i.value for i in ib.accountValues() if i.tag == 'TotalCashValue'][0])

        return balance



    def instruments_info(self, symbol, others='digits'):

        if others == 'digits':
            x = ib.reqContractDetails(self.contract_find(symbol))[0].minTick
            x = abs(decimal.Decimal(x).adjusted())
        else:
            x = ib.reqContractDetails(self.contract_find(symbol))

        return x



    def close_order(self, ID, condition=None):

        for i in ib.openTrades():
            if i.order.ocaGroup == str(ID) and i.order.orderType == 'LMT':
                i.order.update(orderType = 'MKT')
                ib.placeOrder(i.contract, i.order)
            elif condition == 'all':
                i.order.update(orderType = 'MKT')
                ib.placeOrder(i.contract, i.order)
            else:
                pass



    def std_curr(self, symbol):
 
        symbol_data = [self.assets.get(i)[1] for i in self.assets.keys() if i == symbol][0]

        if symbol_data == 'USD':
            return 1
        elif symbol_data[:3] in ['GBP', 'EUR', 'AUD']:
            return 1 / self.candle_data(symbol_data, 1, 2).iloc[-1].close
        else:
            return self.candle_data(symbol_data, 1, 2).iloc[-1].close



    def symbol_fix(self, symbol):

        try:
            symbol = symbol.split('.')[0] + symbol.split('.')[1]
        except:
            symbol = symbol

        return symbol


    
    def last_trade(self, tradeID):

        for i in ib.fills():

            if i.execution.permId == tradeID+1:
                return [i.execution.permId, i.execution.price, self.symbol_fix(i.contract.localSymbol), (i.execution.time + dt.timedelta(hours=3)).time()]
            
            elif i.execution.permId == tradeID+2:
                return [i.execution.permId, i.execution.price, self.symbol_fix(i.contract.localSymbol), (i.execution.time + dt.timedelta(hours=3)).time()]

    

    def trading_hours(self, symbol):

        lt = [i.split(':')[1] for i in self.instruments_info(symbol, 'others')[0].tradingHours.split(';')[0].split('-')]

        start_trade = int(lt[0]) + 300
        
        if start_trade > 2000 and start_trade < 2400:
            start_trade = 0

        end_trade = int(lt[1]) + 300   


        return start_trade, end_trade

