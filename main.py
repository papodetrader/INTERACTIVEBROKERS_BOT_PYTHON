from plan import build_plan
from variable import execution, plan, read_variables

import os
import time
import datetime as dt
import pandas as pd
import pickle
import pytz
import warnings
warnings.filterwarnings("ignore")

# import logging
# logging.basicConfig( filename= (f"./DATA/log/main_{dt.datetime.now(tz=pytz.timezone('Europe/Moscow')).date()}.log"),
#                      filemode='w',
#                      level=logging.ERROR,
#                      format= '%(asctime)s - %(levelname)s - %(message)s',
#                      datefmt= "%Y-%m-%d %H:%M:%S"
#                    )

date_trade = dt.datetime(2014, 4, 24, 8, 0, 0) #dt.datetime.now(tz=pytz.timezone('Europe/Moscow'))

while True:
    starttime = time.time()


    if dt.datetime.now(tz=pytz.timezone('Europe/Moscow')).weekday() in [0, 1, 2, 3, 4]: #date_trade.date()

        if execution.current_time() > 000 and execution.current_time() < 100:
            new_plan = (f'plan_{dt.datetime.now(tz=pytz.timezone("Europe/Moscow")).date()}')
            if new_plan not in os.listdir('./DATA/plan/'):            
                build_plan().run_daily() #date_trade
                read_variables() #date_trade

        else:

            for id in plan: 
                curr = plan[id]['asset']
                
                execution.condition(id, curr) #date_trade

            # if #date_trade.date == #dt.datetime.now(tz=pytz.timezone('Europe/Moscow')).date():
            execution.order_update() 
                    
            execution.day_mgt() #date_trade


        # if #date_trade.date == #dt.datetime.now(tz=pytz.timezone('Europe/Moscow')).date():
        print(f'stopped for {round((60.0 - ((time.time() - starttime) % 60.0)),2)} seconds at {str(execution.current_time())[:-2]+":"+str(execution.current_time())[-2:]} \n')
        time.sleep(60.0 - ((time.time() - starttime) % 60.0))
        #else:
            #date_trade = date_trade + dt.timedelta(minutes=1)

    else:
        print(f'stopped for {round((3600.1 - ((time.time() - starttime) % 60.0)),2)} seconds at {str(execution.current_time())[:-2]+":"+str(execution.current_time())[-2:]} \n')
        time.sleep(3600.1 - ((time.time() - starttime) % 60.0))


        
