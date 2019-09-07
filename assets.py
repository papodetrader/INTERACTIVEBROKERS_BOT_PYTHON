asset = {
            'EURUSD', 'EURAUD', 'EURSEK', 'GBPJPY', 'GBPCAD', 'GBPUSD', 'USDCAD', 'USDJPY', 'AUDJPY', 
            'AUDUSD', 'CHFZAR', 'CHFCNH', 'CHFCZK', 'CHFHUF', 'CHFHUF', 'CHFNOK', 'CHFPLN', 'CHFTRY',
            'EURCNH', 'EURJPY', 'EURGBP', 'EURAUD', 'EURCAD', 'USDCNH', 'CNHJPY', 'CADJPY', 'GBPCNH', 
            'GBPAUD', 'AUDCNH', 'CADCNH',

            'IBUS500', 'IBUST100', 'IBGB100', 'IBDE30', 'IBFR40', 'IBJP225', 'IBHK50', 'IBAU200', 
            # 'XAUUSD': ['CMDTY', 'USD'],
            # 'IBM': ['STK', 'USD'],
            # 'GC': ['Future', 'USD']
        }


assets = {
    'Forex': [['EURUSD', 'EURAUD', 'EURSEK', 'USDCAD', 'USDJPY', 'GBPUSD', 'GBPCAD', 'AUDJPY', 'CHFJPY'], 'IDEALPRO', 'Forex'], 
    'CFD': [['IBUS500', 'IBUST100', 'IBGB100'], 'SMART', 'CFD'],
    'CMDTY': [['XAUUSD', 'XAGUSD'], 'SMART', 'CMDTY'], 
    'Future1': [['GC'], 'NYMEX', 'Future'],
    'Future2': [['ES', 'YM'], 'GLOBEX', 'Future'],
    'Stock': [['IBM', 'C', 'F'], 'NYSE', 'Stock']
}
